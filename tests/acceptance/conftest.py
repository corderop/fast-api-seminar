import pytest
from fastapi.testclient import TestClient
from psycopg import OperationalError

from app import db
from app.auth import config
from app.auth.repositories import users as users_repository
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def database():
    try:
        db.init_schema()
        db.truncate_all()
    except OperationalError as error:
        pytest.fail(
            "PostgreSQL is not reachable. Start it with `docker compose up -d db` "
            f"and check DATABASE_URL. Original error: {error}"
        )

    users_repository.add_user(config.DEFAULT_USERNAME, config.DEFAULT_PASSWORD)
    yield
    db.truncate_all()


@pytest.fixture(autouse=True)
def clean_departments(database):
    db.truncate_departments()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 200

    return {"Authorization": f"Bearer {response.json()['access_token']}"}
