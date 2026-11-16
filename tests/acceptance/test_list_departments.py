from app.factories.departments import create_department


def test_departments_are_listed_in_creation_order(client, auth_headers):
    first = create_department(name="Tecnología", benefits=["Comida"])
    second = create_department(
        name="Recursos Humanos",
        benefits=["Transporte", "Formación"],
    )

    response = client.get("/departments", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == [first, second]


def test_departments_can_be_filtered_by_benefit(client, auth_headers):
    create_department(name="Tecnología", benefits=["Comida"])
    with_transport = create_department(
        name="Recursos Humanos",
        benefits=["Transporte", "Formación"],
    )

    response = client.get(
        "/departments",
        params={"benefit": " transporte "},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == [with_transport]


def test_filtering_by_an_unknown_benefit_returns_an_empty_list(client, auth_headers):
    create_department(name="Tecnología", benefits=["Comida"])

    response = client.get(
        "/departments",
        params={"benefit": "Guardería"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []
