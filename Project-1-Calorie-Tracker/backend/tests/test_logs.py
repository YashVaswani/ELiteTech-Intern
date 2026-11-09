def test_create_and_list_log(client, auth_headers):
    create_response = client.post(
        "/api/logs",
        json={"food_name": "pizza", "serving_grams": 200},
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    body = create_response.json()
    assert body["calories"] == 532.0

    list_response = client.get("/api/logs", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_logs_require_auth(client):
    response = client.get("/api/logs")
    assert response.status_code == 401


def test_create_log_unknown_food_returns_404(client, auth_headers):
    response = client.post(
        "/api/logs",
        json={"food_name": "not_a_real_food", "serving_grams": 100},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_delete_log(client, auth_headers):
    create_response = client.post(
        "/api/logs",
        json={"food_name": "sushi", "serving_grams": 100},
        headers=auth_headers,
    )
    log_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/logs/{log_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    list_response = client.get("/api/logs", headers=auth_headers)
    assert list_response.json() == []


def test_daily_summary(client, auth_headers):
    client.post(
        "/api/logs",
        json={"food_name": "hamburger", "serving_grams": 100},
        headers=auth_headers,
    )
    from datetime import date

    today = date.today().isoformat()
    response = client.get(f"/api/logs/summary/{today}", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total_calories"] == 270.0
    assert len(body["entries"]) == 1
