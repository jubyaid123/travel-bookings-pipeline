def run_quality_checks(df):
    checks = {
        "row_count": len(df) > 0,
        "no_null_arrival_date": df["arrival_date"].notnull().all(),
        "non_negative_guests": (df["total_guests"] >= 0).all(),
        "country_values_present": df["country"].notnull().all(),
    }

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ValueError(f"Data quality checks failed: {failed}")
