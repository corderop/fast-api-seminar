from app.departments.utils import getNextId

_departments: list[dict] = [
    { "id": 1, "name": "Recursos Humanos", "benefits": ["Comida", "Transporte"] }
]


def list_departments() -> list[dict]:
    """Return every department."""
    return _departments


def find_department(department_id: int) -> dict | None:
    """Return the department with the given id, or None when it does not exist."""
    for department in _departments:
        if department["id"] == department_id:
            return department

    return None


def add_department(name: str, benefits: list[str]) -> dict:
    """Create a department and append it to the store."""
    new_department = {
        "id": getNextId(_departments),
        "name": name,
        "benefits": benefits,
    }
    _departments.append(new_department)
    return new_department
