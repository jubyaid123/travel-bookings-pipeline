import pandas as pd

def extract_bookings(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df
