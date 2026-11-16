import random

from app.departments.repositories import departments as departments_repository
from app.factories.fake import fake

BENEFIT_POOL = [
    "Comida",
    "Transporte",
    "Seguro médico",
    "Gimnasio",
    "Formación",
    "Teletrabajo",
    "Seguro dental",
    "Guardería",
    "Bonos de bienestar",
    "Estacionamiento",
]


def department_data(
    name: str | None = None,
    benefits: list[str] | None = None,
) -> dict:
    """Build department data, filling any missing field with fake values."""
    return {
        "name": name if name is not None else fake.company(),
        "benefits": (
            benefits
            if benefits is not None
            else random.sample(BENEFIT_POOL, k=random.randint(1, 5))
        ),
    }


def create_department(
    name: str | None = None,
    benefits: list[str] | None = None,
) -> dict:
    """Persist a department built from explicit or fake data."""
    return departments_repository.add_department(**department_data(name, benefits))
