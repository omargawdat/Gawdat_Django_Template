"""
API Endpoint Smoke Tests

Tests all GET endpoints to ensure they don't crash.
Uses pre-loaded test data from conftest.py fixtures.

To list all endpoints:
    pytest tests/api/test_api_retrieve_endpoints.py::test_list_all_api_endpoints -v -s
"""

import re

import pytest
from django.apps import apps
from django.urls import get_resolver
from rest_framework.test import APIClient

# Map URL segments to Django models (app_label.ModelName)
URL_TO_MODEL_MAP = {
    # Users
    "user": "users.User",
    "users": "users.User",
    "customer": "users.Customer",
    "customers": "users.Customer",
    # Location
    "address": "location.Address",
    "addresses": "location.Address",
    "country": "location.Country",
    "countries": "location.Country",
    "region": "location.Region",
    "regions": "location.Region",
    # Payment
    "wallet": "payment.Wallet",
    "wallets": "payment.Wallet",
    "transaction": "payment.WalletTransaction",
    "transactions": "payment.WalletTransaction",
    # Channel
    "notification": "channel.Notification",
    "notifications": "channel.Notification",
    # AppInfo
    "faq": "appInfo.FAQ",
    "faqs": "appInfo.FAQ",
    "banner": "appInfo.Banner",
    "banners": "appInfo.Banner",
}


def test_list_all_api_endpoints():
    """
    List all API endpoints with their authentication requirements.

    Run with: pytest tests/api/test_api_retrieve_endpoints.py::test_list_all_api_endpoints -v -s
    """
    endpoints = _collect_api_endpoints()

    public = [e for e in endpoints if not e[2]]  # requires_auth=False
    protected = [e for e in endpoints if e[2]]  # requires_auth=True

    print(f"\n{'=' * 100}")
    print(f"📋 TOTAL API ENDPOINTS: {len(endpoints)}")
    print(f"{'=' * 100}")
    print(f"🌐 Public endpoints: {len(public)}")
    print(f"🔒 Protected endpoints: {len(protected)}\n")

    print("🌐 PUBLIC ENDPOINTS:")
    print("-" * 100)
    for url, name, _ in public:
        clean = url.replace("^", "").replace("$", "")
        if not _should_skip_endpoint(url):
            print(f"  GET /{clean:<60} {name or '(unnamed)'}")

    print("\n🔒 PROTECTED ENDPOINTS:")
    print("-" * 100)
    for url, name, _ in protected:
        clean = url.replace("^", "").replace("$", "")
        if not _should_skip_endpoint(url):
            print(f"  GET /{clean:<60} {name or '(unnamed)'}")

    print(f"\n{'=' * 100}\n")


def _collect_api_endpoints():
    """Extract all API endpoints from URL configuration"""
    endpoints = []
    resolver = get_resolver()

    def extract_urls(patterns, prefix=""):
        for pattern in patterns:
            if hasattr(pattern, "url_patterns"):
                # URLResolver (include)
                extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            elif hasattr(pattern, "callback"):
                # URLPattern (actual endpoint)
                url = prefix + str(pattern.pattern)
                name = pattern.name

                # Check if requires auth
                requires_auth = False
                if hasattr(pattern.callback, "cls"):
                    view_class = pattern.callback.cls
                    if hasattr(view_class, "permission_classes"):
                        requires_auth = any(
                            "IsAuthenticated" in str(perm)
                            for perm in view_class.permission_classes
                        )

                endpoints.append((url, name, requires_auth))

    # Find API endpoints
    for pattern in resolver.url_patterns:
        if str(pattern.pattern).startswith("api/"):
            extract_urls(pattern.url_patterns, "api/")

    return endpoints


def _should_skip_endpoint(url_pattern):
    """Check if endpoint should be skipped from testing"""
    skip_patterns = [
        "schema",  # API schema endpoints
        "docs",  # API documentation
        "(?P<",  # Old Django regex patterns
        "swagger",  # Swagger docs
        "redoc",  # ReDoc docs
        "<drf_format_suffix:",  # DRF format suffix (.json, .api)
    ]

    return any(skip in url_pattern for skip in skip_patterns)


def _resolve_url(url_pattern, user):
    """
    Convert URL pattern to actual testable URL.

    Examples:
        api/users/ -> api/users/
        api/users/<int:pk>/ -> api/users/5/
        api/addresses/<int:address_id>/ -> api/addresses/42/

    Args:
        url_pattern: Django URL pattern string
        user: User object to get related data for

    Returns:
        Resolved URL string or None if cannot resolve

    Raises:
        ValueError: If URL cannot be resolved (missing data or mapping)
    """
    # Clean Django URL pattern syntax
    url = url_pattern.replace("^", "").replace("$", "")

    # No parameters - return as-is
    if "<" not in url:
        return url

    # Extract all parameters: <type:name>
    params = re.findall(r"<(\w+):(\w+)>", url)

    if not params:
        raise ValueError("Unknown URL parameter format")

    # Replace each parameter with actual data
    for param_type, param_name in params:
        obj_id = _get_object_id_for_param(param_name, url, user)
        url = url.replace(f"<{param_type}:{param_name}>", str(obj_id))

    return url


def _get_object_id_for_param(param_name, url, user):
    """
    Get object ID for URL parameter from existing test data.

    Args:
        param_name: Parameter name (e.g., 'pk', 'address_id')
        url: Full URL pattern for context
        user: User to filter related objects

    Returns:
        Object ID (primary key)

    Raises:
        ValueError: If no data found or model not mapped
    """
    # Get Django model for this parameter
    model = _get_model_from_param(param_name, url)

    if not model:
        raise ValueError(
            f"No model mapping for '{param_name}'. "
            f"Add to URL_TO_MODEL_MAP in test file."
        )

    # Query existing object for this user
    obj = _get_user_related_object(model, user)

    if not obj:
        raise ValueError(
            f"No {model.__name__} found for user {user.id}. "
            f"Ensure conftest.py creates this data in fixtures."
        )

    return obj.pk


def _get_model_from_param(param_name, url):
    """
    Map URL parameter name to Django model.

    Handles patterns like:
        - address_id -> Address model
        - order_id -> Order model
        - pk -> infer from URL path (e.g., api/users/<pk> -> User)
        - id -> infer from URL path

    Args:
        param_name: Parameter name from URL
        url: Full URL for context

    Returns:
        Django model class or None
    """
    # Handle parameters ending with '_id'
    if param_name.endswith("_id"):
        model_key = param_name[:-3]  # Remove '_id' suffix
        if model_key in URL_TO_MODEL_MAP:
            return apps.get_model(URL_TO_MODEL_MAP[model_key])

    # Handle generic 'pk' or 'id' - infer from URL path
    if param_name in ["pk", "id"]:
        # Extract resource name: 'api/users/<int:pk>/' -> 'users'
        match = re.search(r"api/(\w+)/", url)
        if match:
            resource_name = match.group(1)

            # Try exact match and singular form
            for key in [resource_name, resource_name.rstrip("s")]:
                if key in URL_TO_MODEL_MAP:
                    return apps.get_model(URL_TO_MODEL_MAP[key])

    return None


def _get_user_related_object(model, user):
    """
    Get first object of this model related to the user.

    Automatically detects user relationship fields:
        - user, customer, owner, created_by, author

    If no user relationship exists, returns any first object.

    Args:
        model: Django model class
        user: User to filter by

    Returns:
        Model instance or None
    """
    # Common field names for user foreign keys
    user_field_names = [
        "user",
        "customer",
        "owner",
        "created_by",
        "author",
        "account",
    ]

    # Try each potential user field
    for field_name in user_field_names:
        if hasattr(model, field_name):
            queryset = model.objects.filter(**{field_name: user})
            obj = queryset.first()
            if obj:
                return obj

    # No user relationship - return any object
    return model.objects.first()


@pytest.mark.django_db
class TestAPIEndpoints:
    """Test all API GET endpoints don't crash"""

    def test_all_get_endpoints_dont_crash(self, api_user, api_client_authenticated):
        """
        Hit every GET endpoint and ensure no server errors (500+).
        Tests both authenticated and unauthenticated access.

        Raises AssertionError if:
        - Any endpoint cannot be tested (missing data or mapping)
        - Any endpoint returns 500+ error
        """
        endpoints = _collect_api_endpoints()

        results = {"tested": 0, "errors": [], "untestable": []}

        unauthenticated_client = APIClient()

        for url_pattern, name, requires_auth in endpoints:
            # Skip documentation/schema endpoints
            if _should_skip_endpoint(url_pattern):
                continue

            # Resolve URL with test data
            try:
                url = _resolve_url(url_pattern, api_user)
            except ValueError as e:
                results["untestable"].append(
                    {"name": name, "pattern": url_pattern, "error": str(e)}
                )
                continue

            results["tested"] += 1

            # Test both authenticated and unauthenticated access
            for client, auth_label in [
                (unauthenticated_client, "public"),
                (api_client_authenticated, "authenticated"),
            ]:
                response = client.get(f"/{url}")

                # Only fail on server errors (500+)
                if response.status_code >= 500:
                    results["errors"].append(
                        {
                            "name": name,
                            "url": url,
                            "auth": auth_label,
                            "status": response.status_code,
                        }
                    )

        # Print summary
        self._print_results(results)

        # Assert no failures
        self._assert_no_failures(results)

    def test_public_endpoints_dont_require_auth(self, api_user):
        """Test that public endpoints work without authentication"""
        endpoints = _collect_api_endpoints()
        client = APIClient()

        tested = 0
        failures = []

        for url_pattern, name, requires_auth in endpoints:
            if requires_auth or _should_skip_endpoint(url_pattern):
                continue

            try:
                url = _resolve_url(url_pattern, api_user)
            except ValueError:
                continue  # Skip if can't resolve

            tested += 1
            response = client.get(f"/{url}")

            # Public endpoints should NOT return 401/403
            if response.status_code in [401, 403]:
                failures.append(f"{name} ({url})")

        if failures:
            raise AssertionError(
                "\n❌ Public endpoints requiring auth:\n  • " + "\n  • ".join(failures)
            )

        print(f"\n✅ Public: {tested} endpoints work without auth")

    def test_protected_endpoints_require_auth(self, api_user):
        """Test that protected endpoints block unauthenticated access"""
        endpoints = _collect_api_endpoints()
        client = APIClient()

        tested = 0
        failures = []

        for url_pattern, name, requires_auth in endpoints:
            if not requires_auth or _should_skip_endpoint(url_pattern):
                continue

            try:
                url = _resolve_url(url_pattern, api_user)
            except ValueError:
                continue  # Skip if can't resolve

            tested += 1
            response = client.get(f"/{url}")

            # Protected endpoints MUST return 401/403
            if response.status_code not in [401, 403]:
                failures.append(f"{name} ({url}) returned {response.status_code}")

        if failures:
            raise AssertionError(
                "\n❌ Protected endpoints not requiring auth:\n  • "
                + "\n  • ".join(failures)
            )

        print(f"\n✅ Protected: {tested} endpoints require auth")

    def test_protected_endpoints_work_with_auth(
        self, api_user, api_client_authenticated
    ):
        """Test that protected endpoints work when authenticated"""
        endpoints = _collect_api_endpoints()

        tested = 0
        success = 0
        failures = []

        for url_pattern, name, requires_auth in endpoints:
            if not requires_auth or _should_skip_endpoint(url_pattern):
                continue

            try:
                url = _resolve_url(url_pattern, api_user)
            except ValueError:
                continue  # Skip if can't resolve

            tested += 1
            response = api_client_authenticated.get(f"/{url}")

            # With auth, should NOT return 401/403
            if response.status_code in [401, 403]:
                failures.append(f"{name} ({url}) returned {response.status_code}")
            elif response.status_code == 200:
                success += 1

        if failures:
            raise AssertionError(
                "\n❌ Protected endpoints failing with auth:\n  • "
                + "\n  • ".join(failures)
            )

        print(f"\n✅ Authenticated: {tested} tested, {success} returned 200")

    def _print_results(self, results):
        """Print test results summary"""
        print(f"\n{'=' * 80}")
        print("API Endpoint Smoke Test Results")
        print(f"{'=' * 80}")
        print(f"✅ Tested: {results['tested']} endpoints")

        if results["untestable"]:
            print(f"\n⚠️  Untestable: {len(results['untestable'])} endpoints")
            for item in results["untestable"]:
                print(f"   - {item['name']} ({item['pattern']})")
                print(f"     Error: {item['error']}")

        if results["errors"]:
            print(f"\n❌ Errors: {len(results['errors'])} endpoints")
            for item in results["errors"]:
                print(f"   - {item['name']} ({item['url']})")
                print(f"     Auth: {item['auth']}, Status: {item['status']}")

        if not results["untestable"] and not results["errors"]:
            print("\n🎉 All endpoints passed!")

        print(f"{'=' * 80}\n")

    def _assert_no_failures(self, results):
        """Raise assertion errors if any tests failed"""
        errors = []

        # Check for untestable endpoints
        if results["untestable"]:
            error_lines = ["\n❌ Could not test the following endpoints:"]
            for item in results["untestable"]:
                error_lines.append(f"  • {item['name']} ({item['pattern']})")
                error_lines.append(f"    {item['error']}")
            errors.append("\n".join(error_lines))

        # Check for server errors
        if results["errors"]:
            error_lines = ["\n❌ Endpoints returned server errors:"]
            for item in results["errors"]:
                error_lines.append(
                    f"  • {item['name']} ({item['url']}) "
                    f"[{item['auth']}]: {item['status']}"
                )
            errors.append("\n".join(error_lines))

        if errors:
            raise AssertionError("\n".join(errors))
