from app.factories.departments import create_department


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


def test_department_created_by_a_factory_can_be_retrieved(client):
    department = create_department(
        name="Operaciones",
        benefits=["Comida", "Seguro dental"],
    )

    response = client.get(f"/departments/{department['id']}")

    assert response.status_code == 200
    assert response.json() == department


def test_missing_department_returns_not_found(client):
    response = client.get("/departments/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Department not found"
