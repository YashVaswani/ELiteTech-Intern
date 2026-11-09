import pandas as pd

from retail_segmentation.model import FEATURE_COLUMNS, train


def _fake_rfm(n=60):
    return pd.DataFrame(
        {
            "customer_id": range(n),
            "recency": [5] * (n // 2) + [200] * (n - n // 2),
            "frequency": [20] * (n // 2) + [1] * (n - n // 2),
            "monetary": [1000.0] * (n // 2) + [50.0] * (n - n // 2),
        }
    )


def test_train_produces_requested_cluster_count():
    rfm = _fake_rfm()
    pipeline = train(rfm, n_clusters=2, random_state=42)

    labels = pipeline.named_steps["kmeans"].labels_
    assert len(set(labels)) == 2
    assert len(labels) == len(rfm)


def test_train_pipeline_predicts_on_new_points():
    rfm = _fake_rfm()
    pipeline = train(rfm, n_clusters=2, random_state=42)

    new_point = pd.DataFrame([{"recency": 3, "frequency": 25, "monetary": 1200.0}])
    prediction = pipeline.predict(new_point[FEATURE_COLUMNS])
    assert prediction.shape == (1,)
