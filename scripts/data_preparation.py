"""
Online Retail Customer LTV Analysis - Starter Data Preparation Script

Purpose:
- Load transaction-level retail data
- Apply baseline cleaning rules
- Engineer revenue and customer-level metrics
- Export a Tableau-ready customer dataset

This script is intentionally starter-friendly and can be adapted
for local CSV files or database extracts.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "online_retail_transactions.csv"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "customer_ltv_dataset.csv"


def load_data(path: Path) -> pd.DataFrame:
    """Load raw transaction data from CSV."""
    return pd.read_csv(path)


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Apply basic cleaning and quality filters."""
    cleaned = df.copy()

    # Standardize column names to snake_case for consistency.
    cleaned.columns = [col.strip().lower().replace(" ", "_") for col in cleaned.columns]

    # Required columns check (starter guardrail).
    required_cols = {"customer_id", "invoice_no", "invoice_date", "quantity", "unit_price"}
    missing = required_cols.difference(cleaned.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # Drop records with missing customer id.
    cleaned = cleaned[cleaned["customer_id"].notna()].copy()

    # Standardize types.
    cleaned["invoice_date"] = pd.to_datetime(cleaned["invoice_date"], errors="coerce")
    cleaned["quantity"] = pd.to_numeric(cleaned["quantity"], errors="coerce")
    cleaned["unit_price"] = pd.to_numeric(cleaned["unit_price"], errors="coerce")

    # Remove invalid rows.
    cleaned = cleaned.dropna(subset=["invoice_date", "quantity", "unit_price"])
    cleaned = cleaned[(cleaned["quantity"] > 0) & (cleaned["unit_price"] > 0)]

    # Optional canceled invoice exclusion rule.
    # cleaned = cleaned[~cleaned["invoice_no"].astype(str).str.startswith("C")]

    # Derive year and revenue.
    cleaned["invoice_year"] = cleaned["invoice_date"].dt.year
    cleaned["revenue"] = cleaned["quantity"] * cleaned["unit_price"]

    return cleaned


def build_customer_ltv(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transaction data to customer-level LTV metrics."""
    customer = (
        df.groupby("customer_id", as_index=False)
        .agg(
            customer_ltv=("revenue", "sum"),
            order_frequency=("invoice_no", "nunique"),
        )
        .assign(
            avg_order_value=lambda d: d["customer_ltv"] / d["order_frequency"],
            repeat_customer_flag=lambda d: (d["order_frequency"] > 1).astype(int),
        )
    )

    # LTV bins for distribution view.
    bins = [0, 100, 250, 500, 1000, 2500, float("inf")]
    labels = ["0-99", "100-249", "250-499", "500-999", "1000-2499", "2500+"]
    customer["ltv_bin"] = pd.cut(customer["customer_ltv"], bins=bins, labels=labels, right=False)

    return customer.sort_values("customer_ltv", ascending=False)


def main() -> None:
    """Execute end-to-end transformation and export analytical dataset."""
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Raw file not found: {RAW_PATH}. Place source CSV in data/raw/ and rerun."
        )

    raw_df = load_data(RAW_PATH)
    clean_df = clean_transactions(raw_df)
    customer_df = build_customer_ltv(clean_df)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    customer_df.to_csv(PROCESSED_PATH, index=False)

    # Lightweight KPI printout for quick QA.
    total_customers = customer_df["customer_id"].nunique()
    repeat_customer_pct = customer_df["repeat_customer_flag"].mean()
    average_ltv = customer_df["customer_ltv"].mean()
    average_repeat_ltv = customer_df.loc[
        customer_df["repeat_customer_flag"] == 1, "customer_ltv"
    ].mean()

    print("Customer LTV dataset created successfully.")
    print(f"Output: {PROCESSED_PATH}")
    print(f"Total customers: {total_customers:,}")
    print(f"Average LTV: {average_ltv:,.2f}")
    print(f"Average Repeat LTV: {average_repeat_ltv:,.2f}")
    print(f"Repeat Customer %: {repeat_customer_pct:.2%}")


if __name__ == "__main__":
    main()
