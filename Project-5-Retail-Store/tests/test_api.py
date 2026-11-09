"""Integration tests for the FastAPI layer.

Requires a trained model on disk (run `retail-segment train` first, or rely
on CI's pipeline smoke-test step which does this before pytest runs).
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app
from retail_segmentation.config import load_config


@pytest.fixture(scope="module")
def client():
    cfg = load_config()
    if not Path(cfg["model"]["artifact_path"]).exists():
        pytest.skip("No trained model found; run `retail-segment train` first.")
    with TestClient(app) as c:
        yield c


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.text == '"ok"' or response.text == "ok"


def test_overview(client):
    response = client.get("/api/overview")
    assert response.status_code == 200
    body = response.json()
    assert body["customers"] > 0
    assert body["segments"] > 0


def test_segments_summary(client):
    response = client.get("/api/segments/summary")
    assert response.status_code == 200
    body = response.json()
    assert len(body) > 0
    assert {"segment", "customers", "avg_recency_days", "avg_frequency", "avg_monetary"} <= body[0].keys()


def test_unknown_segment_returns_404(client):
    response = client.get("/api/segments/Not A Real Segment/customers")
    assert response.status_code == 404


def test_clusters(client):
    response = client.get("/api/clusters")
    assert response.status_code == 200
    body = response.json()
    assert len(body) > 0
    assert {"pc1", "pc2", "cluster", "segment"} <= body[0].keys()


def test_predict(client):
    response = client.post("/api/predict", json={"recency": 10, "frequency": 20, "monetary": 2000})
    assert response.status_code == 200
    body = response.json()
    assert "cluster" in body and "segment" in body


def test_predict_rejects_invalid_input(client):
    response = client.post("/api/predict", json={"recency": -5, "frequency": 20, "monetary": 2000})
    assert response.status_code == 422


def test_export_segment_csv(client):
    segment = client.get("/api/segments/summary").json()[0]["segment"]
    response = client.get(f"/api/segments/{segment}/export")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "customer_id" in response.text
