from fastapi.testclient import TestClient

from app.factories.users import create_user
from app.main import app


def test_token_is_issued_for_valid_credentials():
    client = TestClient(app)

    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["expires_in"] > 0


def test_token_is_issued_for_a_user_created_by_a_factory():
    create_user(username="factory-user", password="factory-password")
    client = TestClient(app)

    response = client.post(
        "/auth/token",
        json={"username": "factory-user", "password": "factory-password"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_token_is_rejected_for_invalid_credentials():
    client = TestClient(app)

    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "wrong"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_token_endpoint_requires_a_json_body():
    client = TestClient(app)

    response = client.post("/auth/token", json={"username": "admin"})

    assert response.status_code == 422


def test_protected_endpoint_rejects_missing_token():
    client = TestClient(app)

    response = client.get("/departments")

    assert response.status_code == 401


def test_protected_endpoint_rejects_invalid_token():
    client = TestClient(app)

    response = client.get(
        "/departments",
        headers={"Authorization": "Bearer not-a-jwt"},
    )

    assert response.status_code == 401


def test_protected_endpoint_accepts_issued_token():
    client = TestClient(app)
    token = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin"},
    ).json()["access_token"]

    response = client.get(
        "/departments",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
