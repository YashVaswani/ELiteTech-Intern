import pandas as pd

from retail_segmentation.features import compute_rfm


def test_compute_rfm_basic():
    transactions = pd.DataFrame(
        {
            "customer_id": [1, 1, 2],
            "invoice_date": pd.to_datetime(["2025-12-01", "2025-12-20", "2025-11-01"]),
            "amount": [50.0, 30.0, 100.0],
        }
    )

    rfm = compute_rfm(transactions, snapshot_date="2026-01-01")

    assert set(rfm["customer_id"]) == {1, 2}
    row1 = rfm.set_index("customer_id").loc[1]
    assert row1["frequency"] == 2
    assert row1["monetary"] == 80.0
    assert row1["recency"] == 12  # days between 2025-12-20 and 2026-01-01

    row2 = rfm.set_index("customer_id").loc[2]
    assert row2["frequency"] == 1
    assert row2["monetary"] == 100.0
