import pandas as pd
import re
from datetime import date

INPUT_FILE = "customers.csv"
OUTPUT_FILE = "customers_cleansed.csv"
DUE_SOON_DAYS = 30
DATE_FORMATS = ["%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y"]


def parse_date(value: str) -> pd.Timestamp:
    if not isinstance(value, str) or value.strip() == "":
        return pd.NaT
    for fmt in DATE_FORMATS:
        try:
            return pd.to_datetime(value.strip(), format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT


def cleanse_name(name: str) -> str:
    if not isinstance(name, str):
        return name
    return re.sub(r"\s+", " ", name.strip()).title()


def control_status(days) -> str:
    if days is None or pd.isna(days):
        return "UNKNOWN"
    if days < 0:
        return "OVERDUE"
    if days <= DUE_SOON_DAYS:
        return "DUE_SOON"
    return "OK"


def main():
    df = pd.read_csv(INPUT_FILE, sep=";", dtype=str, keep_default_na=False)
    print(f"Loaded {len(df):,} rows from '{INPUT_FILE}'.")

    df["src_customer_name"] = df["src_customer_name"].apply(cleanse_name)

    date_cols = ["src_date_created", "src_date_last_control", "src_date_next_control"]
    for col in date_cols:
        df[col] = df[col].apply(parse_date)

    today = pd.Timestamp(date.today())
    df["days_until_next_control"] = (df["src_date_next_control"] - today).dt.days
    df["control_status"] = df["days_until_next_control"].apply(control_status)

    print(df["control_status"].value_counts().to_string())
    print(f"Rows with missing next_control date: {df['src_date_next_control'].isna().sum():,}")

    out = df.copy()
    for col in date_cols:
        out[col] = out[col].dt.strftime("%Y-%m-%d")

    out.to_csv(OUTPUT_FILE, sep=";", index=False)
    print(f"\nCleansed file written to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()


