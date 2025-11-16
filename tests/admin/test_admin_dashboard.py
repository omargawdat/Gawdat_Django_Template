"""Test admin dashboard loads."""

import pytest
from django.urls import reverse

HTTP_200_OK = 200


@pytest.mark.django_db
class TestAdminDashboard:
    """Test admin dashboard page."""

    def test_dashboard_loads(self, admin_client):
        """Admin dashboard should load successfully."""
        response = admin_client.get(reverse("admin:index"))
        assert response.status_code == HTTP_200_OK
