"""Turn a transaction log into per-customer RFM features."""

import pandas as pd


def compute_rfm(transactions: pd.DataFrame, snapshot_date: str) -> pd.DataFrame:
    """Aggregate transactions into Recency, Frequency, and Monetary per customer.

    - Recency: days since the customer's most recent purchase (lower = more engaged).
    - Frequency: number of orders placed.
    - Monetary: total amount spent.
    """
    snapshot = pd.Timestamp(snapshot_date)
    rfm = transactions.groupby("customer_id").agg(
        recency=("invoice_date", lambda dates: (snapshot - dates.max()).days),
        frequency=("invoice_date", "count"),
        monetary=("amount", "sum"),
    )
    rfm["monetary"] = rfm["monetary"].round(2)
    return rfm.reset_index()
