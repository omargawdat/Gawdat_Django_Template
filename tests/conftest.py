"""
Pytest fixtures for automatic test data setup

Auto-discovers all factories and creates test data before each test.
Data is automatically cleaned up via Django's transaction rollback.
"""

import inspect

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import RequestFactory
from pytest_factoryboy import register

import factories as factories_module
from factories.loader import load_all_factories

# Auto-register all factories as pytest fixtures
for name, obj in inspect.getmembers(factories_module):
    if (
        inspect.isclass(obj)
        and name.endswith("Factory")
        and hasattr(obj, "_meta")
        and hasattr(obj._meta, "model")
    ):
        register(obj)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Create test data once per test session"""
    with django_db_blocker.unblock():
        load_all_factories(count=2, use_transaction=False)


# Admin-specific fixtures
TEST_PASSWORD = "admin123"  # pragma: allowlist secret # noqa: S105


@pytest.fixture
def admin_user(db):
    """Create superuser"""
    User = get_user_model()
    return User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password=TEST_PASSWORD,
        is_superuser=True,
    )


@pytest.fixture
def admin_client(admin_user):
    """Client logged in as admin"""
    client = Client(raise_request_exception=True)
    client.force_login(admin_user)
    return client


@pytest.fixture
def mock_request(admin_user):
    """Mock request for permission checks"""
    request_factory = RequestFactory()
    request = request_factory.get("/admin/")
    request.user = admin_user
    return request
