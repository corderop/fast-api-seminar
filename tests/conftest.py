import os

# Tests always use their own database so the development data is never touched.
os.environ["DATABASE_URL"] = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://bms:bms@127.0.0.1:5432/bms_test",
)
