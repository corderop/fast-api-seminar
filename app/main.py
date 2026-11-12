from fastapi import FastAPI

from app.departments.controllers.departments import router as departments_router

app = FastAPI(
    title="Benefit Management System API",
    description="API for managing benefit plans",
)

app.include_router(departments_router)
