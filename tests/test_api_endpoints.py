"""
Auto-discover and test ALL API endpoints.

Configuration:
- RETRIEVE_MODELS: Map retrieve endpoints to models with optional user filtering
  Format: {"endpoint-name": {"model": ModelClass, "user_field": "field_name"}}
  - user_field: Filter objects by authenticated user's related field (e.g., "customer")
  - Set user_field to None for public endpoints (no user filtering)
- QUERY_PARAMS: Map endpoints needing query parameters
"""

import logging
from collections import defaultdict
from http import HTTPStatus
from typing import Any

import pytest
from django.urls import NoReverseMatch
from django.urls import URLPattern
from django.urls import URLResolver
from django.urls import get_resolver
from django.urls import reverse

from apps.location.models.address import Address

logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

RETRIEVE_MODELS: dict[str, Any] = {
    "address-detail": {
        "model": Address,
        "user_field": "customer",  # Filter by customer field
    },
}

QUERY_PARAMS: dict[str, dict[str, str]] = {
    "region-by-point": {"lat": "24.774265", "long": "46.738586"},
}


# ============================================================================
# AUTO-DISCOVERY
# ============================================================================


def get_all_api_endpoints() -> list[dict[str, Any]]:
    """Auto-discover all /api/* endpoints."""
    endpoints = []

    def extract(patterns: list) -> None:
        for pattern in patterns:
            if isinstance(pattern, URLResolver):
                extract(pattern.url_patterns)
            elif isinstance(pattern, URLPattern) and pattern.name:
                endpoint = _try_reverse_endpoint(pattern.name)
                if endpoint:
                    endpoints.append(endpoint)

    extract(get_resolver().url_patterns)
    return endpoints


def _try_reverse_endpoint(name: str) -> dict[str, Any] | None:
    """Try to reverse URL pattern with/without pk."""
    # Try without pk (list endpoints)
    try:
        url = reverse(name)
        if url.startswith("/api/"):
            return {"name": name, "url": url, "needs_pk": False}
    except NoReverseMatch:
        # Try with pk (retrieve endpoints)
        try:
            url = reverse(name, kwargs={"pk": 1})
            if url.startswith("/api/"):
                return {
                    "name": name,
                    "url_template": url.replace("/1/", "/{pk}/"),
                    "needs_pk": True,
                }
        except NoReverseMatch:
            # Pattern requires different params (slug, etc.) - skip
            return None

    return None


# ============================================================================
# TESTS
# ============================================================================


@pytest.mark.django_db
class TestAPIEndpoints:
    """Test all API endpoints return 200 OK."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, authenticated_api_client) -> None:
        from apps.users.models.customer import Customer

        self.public_client = api_client
        self.auth_client = authenticated_api_client
        # Get the authenticated user for user-scoped filtering
        # Customer has OneToOne relationship with User
        customer = Customer.objects.filter(is_verified=True).first()
        self.auth_user = customer.user

    def test_all_endpoints(self) -> None:
        """Auto-discover and test all API endpoints."""
        endpoints = get_all_api_endpoints()
        results = defaultdict(list)

        for endpoint in endpoints:
            self._test_endpoint(endpoint, results)

        self._report_and_fail_if_needed(results, len(endpoints))

    def _test_endpoint(self, endpoint: dict, results: dict) -> None:
        """Test a single endpoint and record result."""
        name = endpoint["name"]
        params = QUERY_PARAMS.get(name, {})

        # Handle retrieve endpoints
        if endpoint.get("needs_pk"):
            url = self._get_retrieve_url(endpoint, results)
            if not url:
                return
        else:
            url = endpoint["url"]

        # Test endpoint
        response = self.public_client.get(url, params)

        if response.status_code == HTTPStatus.OK:
            results["passed"].append(name)
            logger.info("✓ %s", name)
        elif response.status_code in {HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN}:
            self._test_with_auth(name, url, params, results)
        elif response.status_code in {HTTPStatus.FOUND, HTTPStatus.METHOD_NOT_ALLOWED}:
            results["skipped"].append(name)
            logger.debug("⊘ %s (%s)", name, response.status_code)
        else:
            results["failed"].append(f"{name}: {response.status_code}")
            logger.error("✗ %s: %s", name, response.status_code)

    def _get_retrieve_url(self, endpoint: dict, results: dict) -> str | None:
        """Get URL for retrieve endpoint with actual object pk."""
        name = endpoint["name"]
        config = RETRIEVE_MODELS.get(name)

        if not config:
            results["missing_models"].append(name)
            return None

        # Extract model and user_field from config
        model = config["model"]
        user_field = config.get("user_field")

        # Get queryset - filter by user if user_field specified
        if user_field:
            # Get the authenticated user's related object (e.g., user.customer)
            user_relation = getattr(self.auth_user, user_field)
            queryset = model.objects.filter(**{user_field: user_relation})
        else:
            queryset = model.objects.all()

        obj = queryset.first()
        if not obj:
            results["failed"].append(f"{name}: No {model.__name__} in DB")
            return None

        return endpoint["url_template"].format(pk=obj.pk)

    def _test_with_auth(self, name: str, url: str, params: dict, results: dict) -> None:
        """Test endpoint with authentication."""
        auth_response = self.auth_client.get(url, params)

        if auth_response.status_code == HTTPStatus.OK:
            results["passed"].append(name)
            logger.info("✓ %s (auth)", name)
        elif auth_response.status_code in {
            HTTPStatus.FOUND,
            HTTPStatus.METHOD_NOT_ALLOWED,
        }:
            results["skipped"].append(name)
            logger.debug("⊘ %s (%s)", name, auth_response.status_code)
        else:
            results["failed"].append(f"{name} (auth): {auth_response.status_code}")
            logger.error("✗ %s (auth): %s", name, auth_response.status_code)

    def _report_and_fail_if_needed(self, results: dict, total: int) -> None:
        """Report results and fail if needed."""
        tested = len(results["passed"]) + len(results["failed"])

        logger.info("\n%s", "=" * 70)
        logger.info(
            "API ENDPOINTS: %d/%d passed (%d skipped)",
            len(results["passed"]),
            tested,
            len(results["skipped"]),
        )
        logger.info("%s\n", "=" * 70)

        if results["missing_models"]:
            self._fail_missing_models(results["missing_models"])

        if results["failed"]:
            self._fail_failed_endpoints(results["failed"])

    def _fail_missing_models(self, missing: list[str]) -> None:
        """Fail with missing model mapping error."""
        message = "\n❌ RETRIEVE endpoints missing model mapping:\n   Add these to RETRIEVE_MODELS:\n\n"
        message += "\n".join(f"   '{name}': YourModel," for name in missing)
        pytest.fail(
            f"{message}\n\n{len(missing)} retrieve endpoint(s) need model mapping"
        )

    def _fail_failed_endpoints(self, failed: list[str]) -> None:
        """Fail with failed endpoints error."""
        message = "\n❌ Failed endpoints:\n"
        message += "\n".join(f"   {fail}" for fail in failed)
        pytest.fail(f"{message}\n\n{len(failed)} endpoint(s) failed")
