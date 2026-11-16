import os
import tempfile
from pathlib import Path

os.environ.setdefault(
    "AUTH_PRIVATE_KEY_FILE",
    str(Path(tempfile.mkdtemp(prefix="bms-auth-")) / "private-key.jwk"),
)
os.environ.setdefault("AUTH_USERNAME", "admin")
os.environ.setdefault("AUTH_PASSWORD", "admin")

# Tests always use their own database so the development data is never touched.
os.environ["DATABASE_URL"] = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://bms:bms@127.0.0.1:5432/bms_test",
)
