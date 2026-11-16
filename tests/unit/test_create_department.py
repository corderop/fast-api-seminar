import pytest

from app.departments.use_cases.create_department import create_department


def test_department_cannot_have_more_than_five_benefits(
    create_department_repository,
):
    benefits = [
        "Comida",
        "Transporte",
        "Seguro médico",
        "Gimnasio",
        "Formación",
        "Teletrabajo",
    ]

    with pytest.raises(ValueError, match="maximum of 5 benefits"):
        create_department(name="Tecnología", benefits=benefits)

    create_department_repository.add_department.assert_not_called()


def test_department_can_be_created_with_less_than_five_benefits(
    create_department_repository,
):
    benefits = ["Comida", "Transporte", "Seguro médico"]
    created_department = {"id": 2, "name": "Tecnología", "benefits": benefits}
    create_department_repository.add_department.return_value = created_department

    department = create_department(name="Tecnología", benefits=benefits)

    assert department == created_department
    create_department_repository.add_department.assert_called_once_with(
        name="Tecnología",
        benefits=benefits,
    )
