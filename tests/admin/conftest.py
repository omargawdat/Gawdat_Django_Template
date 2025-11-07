"""
Admin-specific test fixtures
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import RequestFactory

TEST_PASSWORD = "admin123"  # pragma: allowlist secret # noqa: S105


@pytest.fixture
def admin_user(db):
    """Create superuser"""
    User = get_user_model()
    return User.objects.create_superuser(
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
