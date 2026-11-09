"""Load, or generate, retail transaction data.

No real dataset ships with this repo (avoids licensing issues and keeps the
repo small), so `generate_synthetic_transactions` produces a realistic
transaction log the rest of the pipeline can run against end to end. Point
`load_transactions` at a real export (columns: customer_id, invoice_date,
amount) to use actual store data instead.
"""

import numpy as np
import pandas as pd

_SEGMENT_ARCHETYPES = [
    # name, share of customers, orders/year (rate), spend-per-order (mean, std),
    # inactivity range in years (time since last order), tenure range in days
    # (how long they've been a customer, i.e. how far back orders can date).
    ("champion", 0.10, 30, (150, 15), (0.0, 0.15), (300, 730)),
    ("loyal", 0.20, 14, (80, 12), (0.0, 0.3), (200, 730)),
    ("occasional", 0.30, 6, (40, 8), (0.2, 1.0), (150, 600)),
    ("new", 0.15, 6, (50, 8), (0.0, 0.1), (20, 90)),
    ("at_risk", 0.25, 10, (70, 12), (1.2, 2.5), (200, 600)),
]


def generate_synthetic_transactions(
    n_customers: int, snapshot_date: str, random_state: int = 42
) -> pd.DataFrame:
    """Simulate a transaction log for `n_customers` with distinct buying habits.

    Each customer is drawn from one of a few archetypes (champion, loyal,
    occasional, new, at-risk) so the resulting RFM distribution has genuine
    cluster structure for K-means to recover, instead of pure random noise.
    Order count scales with each customer's tenure (rate * tenure / 365) so
    a "new" customer stays low-frequency because they haven't had time to
    order much yet, not just by chance.
    """
    rng = np.random.default_rng(random_state)
    snapshot = pd.Timestamp(snapshot_date)
    archetype_names = [a[0] for a in _SEGMENT_ARCHETYPES]
    weights = [a[1] for a in _SEGMENT_ARCHETYPES]
    assignments = rng.choice(archetype_names, size=n_customers, p=weights)

    rows = []
    for customer_id, archetype in enumerate(assignments, start=1):
        _, _, orders_per_year, spend_dist, inactive_years_range, tenure_days_range = next(
            a for a in _SEGMENT_ARCHETYPES if a[0] == archetype
        )
        inactive_days = int(rng.uniform(*inactive_years_range) * 365)
        last_active = snapshot - pd.Timedelta(days=inactive_days)
        tenure_days = int(rng.uniform(*tenure_days_range))
        n_orders = max(1, rng.poisson(orders_per_year * tenure_days / 365))
        order_offsets = rng.uniform(0, tenure_days, size=n_orders)
        order_dates = last_active - pd.to_timedelta(order_offsets, unit="D")

        mean_spend, std_spend = spend_dist
        amounts = rng.normal(mean_spend, std_spend, size=n_orders).clip(min=5)

        for date, amount in zip(order_dates, amounts, strict=True):
            rows.append(
                {
                    "customer_id": customer_id,
                    "invoice_date": date.normalize(),
                    "amount": round(float(amount), 2),
                }
            )

    return pd.DataFrame(rows).sort_values(["customer_id", "invoice_date"]).reset_index(drop=True)


def load_transactions(path: str) -> pd.DataFrame:
    """Load a transaction log CSV with columns: customer_id, invoice_date, amount."""
    df = pd.read_csv(path, parse_dates=["invoice_date"])
    required = {"customer_id", "invoice_date", "amount"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Transaction file is missing required columns: {missing}")
    return df
