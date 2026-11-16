from app import db
from app.auth import config
from app.auth.passwords import generate_salt, hash_password


def add_user(username: str, password: str) -> dict:
    """Create a user, storing the salt and password hash separately.

    An existing username is replaced, which makes seeding idempotent.
    """
    salt = generate_salt()

    with db.get_connection() as connection:
        return connection.execute(
            """
            INSERT INTO users (username, salt, password_hash)
            VALUES (%s, %s, %s)
            ON CONFLICT (username) DO UPDATE
                SET salt = EXCLUDED.salt,
                    password_hash = EXCLUDED.password_hash
            RETURNING username, salt, password_hash
            """,
            (username, salt, hash_password(password, salt)),
        ).fetchone()


def find_user(username: str) -> dict | None:
    """Return the user with the given username, or None when it does not exist."""
    with db.get_connection() as connection:
        return connection.execute(
            """
            SELECT username, salt, password_hash
            FROM users
            WHERE username = %s
            """,
            (username,),
        ).fetchone()


def ensure_default_user() -> dict:
    """Create the configured default user when it is missing."""
    user = find_user(config.DEFAULT_USERNAME)

    if user is not None:
        return user

    return add_user(config.DEFAULT_USERNAME, config.DEFAULT_PASSWORD)
