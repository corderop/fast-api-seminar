import argparse

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
