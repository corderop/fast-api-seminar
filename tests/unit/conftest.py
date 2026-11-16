from unittest.mock import patch

import pytest


@pytest.fixture
def users_repository():
    """Mock the user repository used by the authenticate use case."""
    with patch("app.auth.use_cases.authenticate.users_repository") as repository:
        yield repository


@pytest.fixture
def create_department_repository():
    """Mock the department repository used by the create department use case."""
    with patch(
        "app.departments.use_cases.create_department.departments_repository"
    ) as repository:
        yield repository


@pytest.fixture
def get_department_repository():
    """Mock the department repository used by the get department use case."""
    with patch(
        "app.departments.use_cases.get_department.departments_repository"
    ) as repository:
        yield repository


@pytest.fixture
def get_departments_repository():
    """Mock the department repository used by the list departments use case."""
    with patch(
        "app.departments.use_cases.get_departments.departments_repository"
    ) as repository:
        yield repository
