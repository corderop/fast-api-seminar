import pytest
from fastapi.testclient import TestClient

from app.departments.repositories import departments as departments_repository
from app.main import app


@pytest.fixture
def client():
    departments_before = list(departments_repository._departments)
    yield TestClient(app)
    departments_repository._departments.clear()
    departments_repository._departments.extend(departments_before)


def test_created_department_can_be_retrieved(client):
    new_department = {
        "name": "Tecnología",
        "benefits": ["Comida", "Transporte"],
    }

    create_response = client.post("/departments", json=new_department)

    assert create_response.status_code == 201
    created_department = create_response.json()
    assert created_department["name"] == new_department["name"]
    assert created_department["benefits"] == new_department["benefits"]

    get_response = client.get(f"/departments/{created_department['id']}")

    assert get_response.status_code == 200
    assert get_response.json() == created_department
