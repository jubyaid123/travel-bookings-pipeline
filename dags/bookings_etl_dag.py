from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator

from etl.extract import extract_bookings
from etl.transform import transform_bookings
from etl.quality import run_quality_checks
from etl.load_postgres import load_to_postgres

RAW_PATH = "/opt/airflow/data/raw/hotel_bookings.csv"
STAGING_DIR = Path("/opt/airflow/data/staging")
EXTRACT_PATH = STAGING_DIR / "bookings_extracted.parquet"
CLEAN_PATH = STAGING_DIR / "bookings_clean.parquet"

KEEP_COLS = ["hotel", "arrival_date", "country", "is_canceled", "total_guests", "adr"]


def extract_task():
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    df = extract_bookings(RAW_PATH)
    df.to_parquet(EXTRACT_PATH, index=False)


def transform_task():
    df = pd.read_parquet(EXTRACT_PATH)
    df = transform_bookings(df)
    df = df[KEEP_COLS]
    df.to_parquet(CLEAN_PATH, index=False)


def quality_task():
    df = pd.read_parquet(CLEAN_PATH)
    run_quality_checks(df)


def load_task():
    df = pd.read_parquet(CLEAN_PATH)
    load_to_postgres(df)


default_args = {
    "owner": "jubyaid",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="bookings_etl",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["portfolio", "etl"],
) as dag:

    extract = PythonOperator(
        task_id="extract_bookings",
        python_callable=extract_task,
    )

    transform = PythonOperator(
        task_id="transform_bookings",
        python_callable=transform_task,
    )

    quality = PythonOperator(
        task_id="quality_checks",
        python_callable=quality_task,
    )

    load = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_task,
    )

    extract >> transform >> quality >> load
