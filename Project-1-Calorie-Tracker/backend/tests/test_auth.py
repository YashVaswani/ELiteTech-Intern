def test_register_and_login(client):
    register_response = client.post(
        "/api/auth/register", json={"email": "alice@example.com", "password": "password123"}
    )
    assert register_response.status_code == 201
    assert register_response.json()["email"] == "alice@example.com"

    login_response = client.post(
        "/api/auth/login",
        data={"username": "alice@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_duplicate_registration_rejected(client):
    payload = {"email": "bob@example.com", "password": "password123"}
    client.post("/api/auth/register", json=payload)
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 409


def test_login_with_wrong_password_fails(client):
    client.post(
        "/api/auth/register", json={"email": "carol@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/auth/login", data={"username": "carol@example.com", "password": "wrong"}
    )
    assert response.status_code == 401


def test_me_requires_auth(client):
    assert client.get("/api/auth/me").status_code == 401


def test_me_returns_current_user(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
