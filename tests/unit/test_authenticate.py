import jwt
import pytest

from app.auth import config
from app.auth.passwords import generate_salt, hash_password, verify_password
from app.auth.tokens import create_access_token, decode_access_token
from app.auth.use_cases.authenticate import authenticate


def _build_user(username: str = "admin", password: str = "admin") -> dict:
    salt = generate_salt()

    return {
        "username": username,
        "salt": salt,
        "password_hash": hash_password(password, salt),
    }


def test_authenticate_returns_a_valid_token_for_valid_credentials(
    users_repository,
):
    users_repository.find_user.return_value = _build_user()

    response = authenticate(username="admin", password="admin")

    assert response is not None
    assert response["token_type"] == "bearer"
    assert response["expires_in"] == config.TOKEN_TTL_SECONDS

    claims = decode_access_token(response["access_token"])
    assert claims["sub"] == "admin"
    assert claims["iss"] == config.ISSUER
    assert claims["aud"] == config.AUDIENCE
    users_repository.find_user.assert_called_once_with("admin")


def test_authenticate_returns_none_for_a_wrong_password(users_repository):
    users_repository.find_user.return_value = _build_user()

    assert authenticate(username="admin", password="wrong") is None


def test_authenticate_returns_none_for_an_unknown_user(users_repository):
    users_repository.find_user.return_value = None

    assert authenticate(username="nobody", password="admin") is None


def test_password_hashes_are_salted_and_verifiable():
    first_salt = generate_salt()
    second_salt = generate_salt()

    first_hash = hash_password("secret", first_salt)
    second_hash = hash_password("secret", second_salt)

    assert first_salt != second_salt
    assert first_hash != second_hash
    assert verify_password("secret", first_salt, first_hash)
    assert not verify_password("wrong", first_salt, first_hash)


def test_tampered_tokens_are_rejected():
    token, _ = create_access_token(subject="admin")
    header, payload, signature = token.split(".")

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(f"{header}.{payload}.{signature[:-2]}xx")
