from app.departments.repositories import departments as departments_repository


def create_department(name: str, benefits: list[str]) -> dict:
    """Create a new department."""
    if (len(benefits) > 5):
        raise ValueError("A department can have a maximum of 5 benefits.")

    return departments_repository.add_department(name=name, benefits=benefits)
