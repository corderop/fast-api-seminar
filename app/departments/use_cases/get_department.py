from app.departments.repositories import departments as departments_repository


def get_department(department_id: int) -> dict | None:
    """Return a single department, or None when it does not exist."""
    return departments_repository.find_department(department_id)
