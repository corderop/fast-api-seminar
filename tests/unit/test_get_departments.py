from app.departments.use_cases.get_department import get_department
from app.departments.use_cases.get_departments import get_departments


def test_get_department_returns_the_repository_department(get_department_repository):
    department = {"id": 7, "name": "Tecnología", "benefits": ["Comida"]}
    get_department_repository.find_department.return_value = department

    assert get_department(7) == department
    get_department_repository.find_department.assert_called_once_with(7)


def test_get_department_returns_none_when_missing(get_department_repository):
    get_department_repository.find_department.return_value = None

    assert get_department(404) is None


def test_get_departments_passes_the_benefit_filter(get_departments_repository):
    departments = [{"id": 1, "name": "Tecnología", "benefits": ["Comida"]}]
    get_departments_repository.list_departments.return_value = departments

    assert get_departments(benefit="Comida") == departments
    get_departments_repository.list_departments.assert_called_once_with(
        benefit="Comida"
    )
