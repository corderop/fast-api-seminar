import time

import jwt

from app.auth import config, keys


def create_access_token(subject: str) -> tuple[str, int]:
    """Return a signed access token for a subject and its lifetime in seconds."""
    issued_at = int(time.time())
    expires_in = config.TOKEN_TTL_SECONDS
    payload = {
        "sub": subject,
        "iss": config.ISSUER,
        "aud": config.AUDIENCE,
        "iat": issued_at,
        "exp": issued_at + expires_in,
    }

    token = jwt.encode(
        payload,
        keys.get_signing_key(),
        algorithm=keys.ALGORITHM,
        headers={"kid": keys.KEY_ID},
    )

    return token, expires_in


def decode_access_token(token: str) -> dict:
    """Validate a token against the published JWK and return its claims."""
    header = jwt.get_unverified_header(token)
    verification_key = keys.get_verification_key(header.get("kid"))

    return jwt.decode(
        token,
        verification_key,
        algorithms=[keys.ALGORITHM],
        issuer=config.ISSUER,
        audience=config.AUDIENCE,
        options={"require": ["sub", "iss", "aud", "iat", "exp"]},
    )
