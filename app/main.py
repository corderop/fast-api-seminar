from fastapi import FastAPI, status

app = FastAPI(
    title="Benefit Management System API",
    description="API for managing benefit plans",
)

departments = [
    { "id": 1, "name": "Recursos Humanos", "benefits": ["Comida", "Transporte"] }
]

@app.get("/departments", status_code=status.HTTP_200_OK)
def get_departments() -> dict:
    return departments
