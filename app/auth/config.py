import os
from pathlib import Path

ISSUER = os.getenv("AUTH_ISSUER", "benefit-management-system")
AUDIENCE = os.getenv("AUTH_AUDIENCE", "benefit-management-system-api")
TOKEN_TTL_SECONDS = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", "3600"))

DEFAULT_USERNAME = os.getenv("AUTH_USERNAME", "admin")
DEFAULT_PASSWORD = os.getenv("AUTH_PASSWORD", "admin")

PRIVATE_KEY_JWK = os.getenv("AUTH_PRIVATE_KEY_JWK")
PRIVATE_KEY_FILE = Path(
    os.getenv("AUTH_PRIVATE_KEY_FILE", ".auth/private-key.jwk")
)
