from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.auth.use_cases.authenticate import authenticate as authenticate_use_case

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenRequest(BaseModel):
    username: str
    password: str


@router.post("/token", status_code=status.HTTP_200_OK)
def create_token(credentials: TokenRequest) -> dict:
    token = authenticate_use_case(
        username=credentials.username,
        password=credentials.password,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token
