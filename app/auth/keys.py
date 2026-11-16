from functools import lru_cache

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.algorithms import RSAAlgorithm

from app.auth import config

ALGORITHM = "RS256"
KEY_ID = "primary"


@lru_cache(maxsize=1)
def _private_key() -> rsa.RSAPrivateKey:
    """Load the signing key from the environment or the JWK file, creating it once if needed."""
    if config.PRIVATE_KEY_JWK:
        return RSAAlgorithm.from_jwk(config.PRIVATE_KEY_JWK)

    if config.PRIVATE_KEY_FILE.exists():
        return RSAAlgorithm.from_jwk(config.PRIVATE_KEY_FILE.read_text())

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_jwk = RSAAlgorithm.to_jwk(key)

    config.PRIVATE_KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    config.PRIVATE_KEY_FILE.write_text(private_jwk)
    config.PRIVATE_KEY_FILE.chmod(0o600)

    return key


def get_signing_key() -> rsa.RSAPrivateKey:
    """Return the private key used to sign access tokens."""
    return _private_key()


def get_verification_key(key_id: str | None = None) -> rsa.RSAPublicKey:
    """Return the public key matching a token's `kid`."""
    if key_id not in (None, KEY_ID):
        raise jwt.InvalidTokenError("Unknown signing key")

    return _private_key().public_key()
