from app.departments.repositories import departments as departments_repository


def get_departments() -> list[dict]:
    """Return every department."""
    return departments_repository.list_departments()
