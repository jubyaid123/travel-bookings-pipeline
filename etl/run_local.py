from etl.extract import extract_bookings
from etl.transform import transform_bookings
from etl.quality import run_quality_checks
from etl.load_postgres import load_to_postgres

RAW_PATH = "data/raw/hotel_bookings.csv"

def main():
    df = extract_bookings(RAW_PATH)
    df = transform_bookings(df)
    run_quality_checks(df)
    load_to_postgres(df)
    print("✅ Local ETL completed and loaded into Postgres.")

if __name__ == "__main__":
    main()
