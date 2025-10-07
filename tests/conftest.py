"""
Pytest fixtures for automatic test data setup

Auto-discovers all factories and creates test data before each test.
Data is automatically cleaned up via Django's transaction rollback.

For minimal maintenance:
- New factories are auto-discovered and registered
- Test data is auto-loaded once per test session
- Admin tests auto-discover new models
- No test file changes needed when adding models
"""

import inspect

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import RequestFactory
from pytest_factoryboy import register

import factories as factories_module
from factories.loader import load_all_factories

# ============================================================================
# AUTO-REGISTER FACTORIES (minimal maintenance)
# ============================================================================
# Automatically discovers and registers all factories from factories module.
# This makes pytest-factoryboy fixtures available (e.g., customer, address)
# for tests that need custom data.

for name, obj in inspect.getmembers(factories_module):
    if (
        inspect.isclass(obj)
        and name.endswith("Factory")
        and hasattr(obj, "_meta")
        and hasattr(obj._meta, "model")
    ):
        register(obj)


# ============================================================================
# AUTO-LOAD TEST DATA (minimal maintenance)
# ============================================================================


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Automatically load all factory test data once per test session.

    - autouse=True: Runs automatically, no need to inject in tests
    - scope="session": Data loaded once, shared across all tests
    - Tests access data via Model.objects.first(), etc.

    When you add a new factory, it's automatically loaded - zero maintenance!
    """
    with django_db_blocker.unblock():
        load_all_factories(factor=1)


# ============================================================================
# ADMIN FIXTURES
# ============================================================================

TEST_PASSWORD = "admin123"  # pragma: allowlist secret # noqa: S105


@pytest.fixture
def admin_user(db):
    """Create superuser for admin testing"""
    User = get_user_model()
    return User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password=TEST_PASSWORD,
        is_superuser=True,
    )


@pytest.fixture
def admin_client(admin_user):
    """HTTP client authenticated as admin user"""
    client = Client(raise_request_exception=True)
    client.force_login(admin_user)
    return client


@pytest.fixture
def mock_request(admin_user):
    """Mock HTTP request with admin user for permission checks"""
    request_factory = RequestFactory()
    request = request_factory.get("/admin/")
    request.user = admin_user
    return request
