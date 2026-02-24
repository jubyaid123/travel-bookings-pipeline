import os
from sqlalchemy import create_engine

def load_to_postgres(df):
    conn = os.getenv(
        "BOOKINGS_DB_URL",
        "postgresql://postgres:postgres@host.docker.internal:5432/bookings"
    )
    engine = create_engine(conn)
    df.to_sql("fact_bookings", engine, if_exists="replace", index=False)
