import pandas as pd

def transform_bookings(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.lower() for c in df.columns]

    df["arrival_date"] = pd.to_datetime(
        df["arrival_date_year"].astype(str) + "-" +
        df["arrival_date_month"] + "-" +
        df["arrival_date_day_of_month"].astype(str),
        errors="coerce"
    )

    df["is_canceled"] = df["is_canceled"].astype(bool)
    df["total_guests"] = (
        df["adults"] + df["children"].fillna(0) + df["babies"]
    )

    df["country"] = df["country"].fillna("UNK")


    return df
