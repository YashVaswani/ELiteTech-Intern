def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_gestures(client):
    resp = client.get("/api/v1/gestures")
    assert resp.status_code == 200
    assert "open_palm" in resp.json()["gestures"]
