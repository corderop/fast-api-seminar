from app.auth.repositories import users as users_repository
from app.factories.fake import fake


def user_data(
    username: str | None = None,
    password: str | None = None,
) -> dict:
    """Build user data, filling any missing field with fake values."""
    return {
        "username": username if username is not None else fake.user_name(),
        "password": password if password is not None else fake.password(),
    }


def create_user(
    username: str | None = None,
    password: str | None = None,
) -> dict:
    """Persist a user built from explicit or fake data."""
    data = user_data(username, password)

    return users_repository.add_user(**data)
