import argparse
import random

import uvicorn


def _run_pytest(default_path: str) -> None:
    import sys

    import pytest

    targets = sys.argv[1:] or [default_path]
    raise SystemExit(pytest.main(["-v", *targets]))


def test_unit() -> None:
    """Run the unit test suite, optionally scoped to specific paths or pytest options."""
    _run_pytest("tests/unit")


def test_acceptance() -> None:
    """Run the acceptance test suite, optionally scoped to specific paths or pytest options."""
    _run_pytest("tests/acceptance")


def dev() -> None:
    """Run the API locally with auto-reload."""
    parser = argparse.ArgumentParser(
        prog="dev",
        description="Run the Benefit Management System API locally.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    args = parser.parse_args()

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=not args.no_reload,
    )


def db_init() -> None:
    """Create the schema and reset the default user to the configured credentials."""
    from app import db
    from app.auth import config
    from app.auth.repositories import users as users_repository

    db.init_schema()
    user = users_repository.add_user(
        config.DEFAULT_USERNAME,
        config.DEFAULT_PASSWORD,
    )
    print(f"Database ready. Default user: {user['username']}")


def seed() -> None:
    """Populate the database with fake departments and users."""
    from faker import Faker

    from app import db
    from app.auth.repositories import users as users_repository
    from app.factories import departments as department_factory
    from app.factories import users as user_factory

    parser = argparse.ArgumentParser(
        prog="seed",
        description="Populate the database with fake departments and users.",
    )
    parser.add_argument(
        "--departments",
        type=int,
        default=20,
        help="Number of departments to create (default: 20)",
    )
    parser.add_argument(
        "--users",
        type=int,
        default=5,
        help="Number of users to create, in addition to the default user (default: 5)",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Delete existing rows before seeding",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=None,
        help="Seed the fake data generators for reproducible output",
    )
    args = parser.parse_args()

    if args.random_seed is not None:
        random.seed(args.random_seed)
        Faker.seed(args.random_seed)

    db.init_schema()

    if args.clear:
        db.truncate_all()

    users_repository.ensure_default_user()

    for _ in range(args.users):
        user_factory.create_user()

    departments = [
        department_factory.create_department() for _ in range(args.departments)
    ]

    print(
        f"Seeded {len(departments)} departments and {args.users} users."
    )
