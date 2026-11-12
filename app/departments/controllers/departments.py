from fastapi import APIRouter, HTTPException, status

from app.departments.use_cases.create_department import (
    create_department as create_department_use_case,
)
from app.departments.use_cases.get_department import (
    get_department as get_department_use_case,
)
from app.departments.use_cases.get_departments import (
    get_departments as get_departments_use_case,
)

router = APIRouter(prefix="/departments")


@router.get("", status_code=status.HTTP_200_OK)
def get_departments() -> list[dict]:
    return get_departments_use_case()


@router.get("/{department_id}", status_code=status.HTTP_200_OK)
def get_department(department_id: int) -> dict:
    department = get_department_use_case(department_id)

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    return department


@router.post("", status_code=status.HTTP_201_CREATED)
def create_department(department: dict) -> dict:
    try:
        return create_department_use_case(
            name=department["name"],
            benefits=department["benefits"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
