from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_when_model_missing():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_reports_model_loaded(stub_model):
    response = client.get("/health")
    assert response.json()["model_loaded"] is True


def test_predict_without_model_returns_503(monkeypatch):
    from app import inference

    monkeypatch.setattr(inference, "is_model_available", lambda: False)
    response = client.post(
        "/predict", files={"file": ("test.jpg", b"not a real model file", "image/jpeg")}
    )
    assert response.status_code == 503


def test_predict_rejects_unsupported_content_type(stub_model):
    response = client.post("/predict", files={"file": ("test.txt", b"hello", "text/plain")})
    assert response.status_code == 415


def test_predict_rejects_corrupted_image(stub_model):
    response = client.post(
        "/predict", files={"file": ("test.jpg", b"not a real image", "image/jpeg")}
    )
    assert response.status_code == 400


def test_predict_returns_label_and_confidence(stub_model, sample_image_bytes):
    response = client.post(
        "/predict", files={"file": ("test.jpg", sample_image_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["label"] == "dog"
    assert body["confidence"] == 0.8
    assert set(body["probabilities"]) == {"cat", "dog"}
