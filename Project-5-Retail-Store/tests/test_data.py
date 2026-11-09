from retail_segmentation.data import generate_synthetic_transactions


def test_generate_synthetic_transactions_shape_and_columns():
    df = generate_synthetic_transactions(n_customers=50, snapshot_date="2026-01-01", random_state=1)

    assert set(df.columns) == {"customer_id", "invoice_date", "amount"}
    assert df["customer_id"].nunique() == 50
    assert (df["amount"] > 0).all()


def test_generate_synthetic_transactions_is_deterministic():
    df1 = generate_synthetic_transactions(n_customers=30, snapshot_date="2026-01-01", random_state=7)
    df2 = generate_synthetic_transactions(n_customers=30, snapshot_date="2026-01-01", random_state=7)

    assert df1.equals(df2)
