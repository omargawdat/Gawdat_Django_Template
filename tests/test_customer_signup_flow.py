"""Integration test for complete customer profile setup flow."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from apps.location.models.country import Country

User = get_user_model()


@pytest.mark.django_db
class TestCustomerProfileSetup:
    """Test the customer profile setup flow (after authentication)."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        """Setup test data."""
        self.client = api_client
        self.test_email = "newcustomer@test.com"
        self.test_password = "SecurePass123!"  # noqa: S105 # pragma: allowlist secret

        # Get or create a test country
        self.country = Country.objects.filter(is_active=True).first()
        if not self.country:
            pytest.skip("No active country in database. Run seed_db first.")

    def test_complete_customer_profile_setup_flow(self):
        """Test the complete flow: create user → complete profile → get profile → update profile."""

        # ====================================================================
        # STEP 1: Create authenticated user (simulating post-allauth signup)
        # ====================================================================
        user = User.objects.create_user(
            email=self.test_email, password=self.test_password
        )
        self.client.force_authenticate(user=user)

        # User should NOT have a customer profile yet
        assert not hasattr(user, "customer"), "Customer profile should not exist yet"

        # ====================================================================
        # STEP 2: Complete customer profile
        # ====================================================================
        profile_data = {
            "country": self.country.pk,
            "language": "en",
        }

        profile_response = self.client.post(
            "/api/customers/setup/", profile_data, format="json"
        )

        assert profile_response.status_code == status.HTTP_201_CREATED, (
            f"Profile completion failed: {profile_response.status_code} - {profile_response.content}"
        )

        # Verify customer was created
        user.refresh_from_db()
        assert hasattr(user, "customer"), "Customer profile should be created"
        customer = user.customer
        assert customer.country == self.country
        assert user.language == "en"

        # ====================================================================
        # STEP 3: Get customer profile
        # ====================================================================
        profile_get_response = self.client.get("/api/customers/me/")

        assert profile_get_response.status_code == status.HTTP_200_OK, (
            f"Get profile failed: {profile_get_response.status_code} - {profile_get_response.content}"
        )

        # Use .json() method to parse JSON response
        profile = profile_get_response.json()
        assert profile["email"] == self.test_email
        assert profile["country"]["code"] == self.country.code
        assert profile["language"] == "en"

        # ====================================================================
        # STEP 4: Update customer profile
        # ====================================================================
        update_data = {
            "full_name": "John Doe",
            "language": "ar",
        }

        update_response = self.client.patch(
            "/api/customers/me/update/", update_data, format="json"
        )

        assert update_response.status_code == status.HTTP_200_OK, (
            f"Profile update failed: {update_response.status_code} - {update_response.content}"
        )

        updated_profile = update_response.json()
        assert updated_profile["fullName"] == "John Doe"  # API uses camelCase
        assert updated_profile["language"] == "ar"

    def test_complete_profile_twice_fails(self):
        """Test that completing profile twice returns error."""
        # Create and authenticate user
        user = User.objects.create_user(
            email=self.test_email, password=self.test_password
        )
        self.client.force_authenticate(user=user)

        # Complete profile first time
        profile_data = {
            "country": self.country.pk,
            "language": "en",
        }

        first_response = self.client.post(
            "/api/customers/setup/", profile_data, format="json"
        )
        assert first_response.status_code == status.HTTP_201_CREATED

        # Try to complete profile again
        second_response = self.client.post(
            "/api/customers/setup/", profile_data, format="json"
        )
        assert second_response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already completed" in str(second_response.content).lower()

    def test_complete_profile_requires_authentication(self):
        """Test that profile completion requires authentication."""
        profile_data = {
            "country": self.country.pk,
        }

        response = self.client.post(
            "/api/customers/setup/", profile_data, format="json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_profile_requires_authentication(self):
        """Test that getting profile requires authentication."""
        response = self.client.get("/api/customers/me/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_complete_profile_with_invalid_country(self):
        """Test that profile completion fails with invalid country."""
        user = User.objects.create_user(
            email=self.test_email, password=self.test_password
        )
        self.client.force_authenticate(user=user)

        profile_data = {
            "country": 99999,  # Non-existent country
            "language": "en",
        }

        response = self.client.post(
            "/api/customers/setup/", profile_data, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
