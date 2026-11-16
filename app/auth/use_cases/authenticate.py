from app.auth.passwords import verify_password
from app.auth.repositories import users as users_repository
from app.auth.tokens import create_access_token


def authenticate(username: str, password: str) -> dict | None:
    """Return a token response for valid credentials, or None when they are invalid."""
    user = users_repository.find_user(username)

    if user is None or not verify_password(
        password,
        user["salt"],
        user["password_hash"],
    ):
        return None

    access_token, expires_in = create_access_token(subject=user["username"])

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in,
    }
