from fastapi import FastAPI

from app.auth.controllers.auth import router as auth_router
from app.departments.controllers.departments import router as departments_router

app = FastAPI(
    title="Benefit Management System API",
    description="API for managing benefit plans",
)

app.include_router(auth_router)
app.include_router(departments_router)
