from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, field_validator

from app.auth.dependencies import get_current_user
from app.departments.use_cases.create_department import (
    create_department as create_department_use_case,
)
from app.departments.use_cases.get_department import (
    get_department as get_department_use_case,
)
from app.departments.use_cases.get_departments import (
    get_departments as get_departments_use_case,
)

router = APIRouter(
    prefix="/departments",
    dependencies=[Depends(get_current_user)],
)


class CreateDepartmentRequest(BaseModel):
    name: str
    benefits: list[str]

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        name = name.strip()

        if not name:
            raise ValueError("Department name must not be blank.")

        return name

    @field_validator("benefits")
    @classmethod
    def validate_benefits(cls, benefits: list[str]) -> list[str]:
        benefits = [benefit.strip() for benefit in benefits]

        if any(not benefit for benefit in benefits):
            raise ValueError("Benefits must not be blank.")

        return benefits


@router.get("", status_code=status.HTTP_200_OK)
def get_departments(benefit: str | None = Query(default=None)) -> list[dict]:
    return get_departments_use_case(benefit=benefit)


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
def create_department(department: CreateDepartmentRequest) -> dict:
    try:
        return create_department_use_case(
            name=department.name,
            benefits=department.benefits,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
