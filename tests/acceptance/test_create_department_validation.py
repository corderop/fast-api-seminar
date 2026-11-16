import pytest


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"name": "Tecnología"},
        {"benefits": ["Comida"]},
        {"name": "Tecnología", "benefits": "Comida"},
        {"name": "Tecnología", "benefits": [1, 2]},
        {"name": "   ", "benefits": ["Comida"]},
        {"name": "Tecnología", "benefits": ["Comida", "   "]},
    ],
)
def test_create_department_rejects_invalid_payload(client, auth_headers, payload):
    response = client.post("/departments", json=payload, headers=auth_headers)

    assert response.status_code == 422


def test_create_department_trims_whitespace_from_name_and_benefits(
    client, auth_headers
):
    payload = {
        "name": "  Tecnología  ",
        "benefits": ["  Comida  ", " Transporte "],
    }

    response = client.post("/departments", json=payload, headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["name"] == "Tecnología"
    assert response.json()["benefits"] == ["Comida", "Transporte"]


def test_create_department_rejects_more_than_five_benefits(client, auth_headers):
    payload = {
        "name": "Tecnología",
        "benefits": [
            "Comida",
            "Transporte",
            "Seguro médico",
            "Gimnasio",
            "Formación",
            "Teletrabajo",
        ],
    }

    response = client.post("/departments", json=payload, headers=auth_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "A department can have a maximum of 5 benefits."
