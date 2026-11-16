from unittest.mock import patch

from app.auth import config
from app.auth.passwords import verify_password
from app.auth.repositories import users as users_repository
from app.auth.repositories.users import add_user, find_user


def test_add_user_stores_a_salt_and_password_hash():
    stored_user = {
        "username": "alice",
        "salt": "a-salt",
        "password_hash": "a-hash",
    }

    with patch(
        "app.auth.repositories.users.db.get_connection"
    ) as get_connection:
        connection = get_connection.return_value.__enter__.return_value
        connection.execute.return_value.fetchone.return_value = stored_user

        assert add_user("alice", "secret") == stored_user

    params = connection.execute.call_args.args[1]
    assert params[0] == "alice"
    assert verify_password("secret", params[1], params[2])


def test_find_user_returns_the_stored_row():
    stored_user = {
        "username": "alice",
        "salt": "a-salt",
        "password_hash": "a-hash",
    }

    with patch(
        "app.auth.repositories.users.db.get_connection"
    ) as get_connection:
        connection = get_connection.return_value.__enter__.return_value
        connection.execute.return_value.fetchone.return_value = stored_user

        assert find_user("alice") == stored_user

    params = connection.execute.call_args.args[1]
    assert params == ("alice",)


def test_ensure_default_user_reuses_an_existing_user():
    existing_user = {"username": config.DEFAULT_USERNAME}

    with patch(
        "app.auth.repositories.users.find_user",
        return_value=existing_user,
    ) as find_user_mock, patch(
        "app.auth.repositories.users.add_user"
    ) as add_user_mock:
        assert users_repository.ensure_default_user() == existing_user

    find_user_mock.assert_called_once_with(config.DEFAULT_USERNAME)
    add_user_mock.assert_not_called()


def test_ensure_default_user_creates_a_missing_user():
    created_user = {"username": config.DEFAULT_USERNAME}

    with patch(
        "app.auth.repositories.users.find_user",
        return_value=None,
    ), patch(
        "app.auth.repositories.users.add_user",
        return_value=created_user,
    ) as add_user_mock:
        assert users_repository.ensure_default_user() == created_user

    add_user_mock.assert_called_once_with(
        config.DEFAULT_USERNAME,
        config.DEFAULT_PASSWORD,
    )
