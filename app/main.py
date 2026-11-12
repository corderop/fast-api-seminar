from fastapi import FastAPI, HTTPException, status

from app.utils import getNextId

app = FastAPI(
    title="Benefit Management System API",
    description="API for managing benefit plans",
)

departments = [
    { "id": 1, "name": "Recursos Humanos", "benefits": ["Comida", "Transporte"] }
]

@app.get("/departments", status_code=status.HTTP_200_OK)
def get_departments() -> list[dict]:
    return departments

@app.get("/departments/{department_id}", status_code=status.HTTP_200_OK)
def get_department(department_id: int) -> dict:
    for department in departments:
        if department["id"] == department_id:
            return department

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Department not found",
    )

@app.post("/departments", status_code=status.HTTP_201_CREATED)
def create_department(department: dict) -> dict:
    new_department = {
        "id": getNextId(departments),
        "name": department["name"],
        "benefits": department["benefits"],
    }
    departments.append(new_department)
    return new_department
