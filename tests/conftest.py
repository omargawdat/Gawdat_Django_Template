import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import RequestFactory

# ============================================================================
# AUTO-LOAD TEST DATA (minimal maintenance)
# ============================================================================


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Automatically load all factory test data once per test session.

    Uses seed_db command to ensure consistent data loading with flush.
    """
    with django_db_blocker.unblock():
        from io import StringIO

        from django.core.management import call_command

        # Suppress command output in tests
        call_command("seed_db", count=10, flush=False, stdout=StringIO())


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
