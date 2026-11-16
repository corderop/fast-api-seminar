import hashlib
import hmac
import secrets

# Each password guess must pay this cost. Higher is safer but slower.
ITERATIONS = 600_000


def generate_salt() -> str:
    """Return a random salt, unique per user."""
    return secrets.token_hex(16)


def hash_password(password: str, salt: str) -> str:
    """Hash a password with its salt using PBKDF2-SHA256."""
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt),
        ITERATIONS,
    ).hex()


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    """Hash the given password with the stored salt and compare it safely."""
    return hmac.compare_digest(hash_password(password, salt), expected_hash)
