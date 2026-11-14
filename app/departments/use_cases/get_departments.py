from app.departments.repositories import departments as departments_repository


def get_departments(benefit: str | None = None) -> list[dict]:
    """Return every department, optionally filtered by a benefit."""
    return departments_repository.list_departments(benefit=benefit)
