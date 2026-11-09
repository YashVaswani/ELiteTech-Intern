import io

import pytest
from PIL import Image


def _jpeg_bytes() -> io.BytesIO:
    buf = io.BytesIO()
    Image.new("RGB", (64, 64), color=(255, 0, 0)).save(buf, format="JPEG")
    buf.seek(0)
    return buf


def test_predict_image_returns_prediction(client):
    resp = client.post(
        "/api/v1/predict/image",
        files={"file": ("test.jpg", _jpeg_bytes(), "image/jpeg")},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["gesture"] == "open_palm"
    assert body["confidence"] == pytest.approx(0.99)
    assert len(body["landmarks"]) == 21


def test_predict_image_rejects_invalid_file(client):
    resp = client.post(
        "/api/v1/predict/image",
        files={"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")},
    )
    assert resp.status_code == 400


def test_predict_stream_roundtrip(client):
    with client.websocket_connect("/api/v1/predict/stream") as ws:
        ws.send_bytes(_jpeg_bytes().read())
        data = ws.receive_json()
        assert data["gesture"] == "open_palm"
