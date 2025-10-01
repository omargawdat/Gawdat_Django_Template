"""
Admin tests - separated into individual test functions for better reporting
"""

import pytest
from django.contrib import admin
from django.test import Client
from django.test import RequestFactory
from django.urls import reverse

HTTP_200_OK = 200
HTTP_302_FOUND = 302
HTTP_403_FORBIDDEN = 403
TEST_PASSWORD = "admin123"  # pragma: allowlist secret # noqa: S105


@pytest.fixture
def admin_user(db):
    """Create superuser"""
    from django.contrib.auth import get_user_model

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


@pytest.mark.django_db
def test_admin_index(admin_client):
    """Test admin index page loads"""
    response = admin_client.get(reverse("admin:index"))
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_models_have_test_data():
    """Check that all registered models have test data"""
    # Third-party and built-in models to ignore
    IGNORED_MODELS = {
        "fcm_django.fcmdevice",
        "authtoken.tokenproxy",
        "token_blacklist.outstandingtoken",
        "token_blacklist.blacklistedtoken",
        "django_tasks_database.dbtaskresult",
        "account.emailaddress",
        "socialaccount.socialapp",
        "socialaccount.socialtoken",
        "socialaccount.socialaccount",
        "auth.group",
    }

    models_without_data = []

    for model in admin.site._registry:
        if hasattr(model, "objects"):
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            full_name = f"{app_label}.{model_name}"

            # Skip ignored models
            if full_name in IGNORED_MODELS:
                continue

            count = model.objects.count()
            if count == 0:
                models_without_data.append(full_name)

    if models_without_data:
        message = (
            f"\n⚠️  Models without test data ({len(models_without_data)}):\n  - "
            + "\n  - ".join(models_without_data)
        )
        pytest.fail(message)


@pytest.mark.django_db
def test_admin_list_pages(admin_client):
    """Test all admin changelist pages load"""
    for model in admin.site._registry:
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        url = reverse(f"admin:{app_label}_{model_name}_changelist")
        response = admin_client.get(url)
        assert response.status_code in [HTTP_200_OK, HTTP_302_FOUND], (
            f"List page failed for {app_label}.{model_name}"
        )


@pytest.mark.django_db
def test_admin_search(admin_client):
    """Test search functionality on admin pages"""
    for model, model_admin in admin.site._registry.items():
        if hasattr(model_admin, "search_fields") and model_admin.search_fields:
            app_label = model._meta.app_label
            model_name = model._meta.model_name

            url = reverse(f"admin:{app_label}_{model_name}_changelist")
            response = admin_client.get(url, {"q": "test"})
            assert response.status_code == HTTP_200_OK, (
                f"Search failed for {app_label}.{model_name}"
            )


@pytest.mark.django_db
def test_admin_add_pages(admin_client, mock_request):
    """Test add pages (only if user has permission)"""
    for model, model_admin in admin.site._registry.items():
        if model_admin.has_add_permission(mock_request):
            app_label = model._meta.app_label
            model_name = model._meta.model_name

            url = reverse(f"admin:{app_label}_{model_name}_add")
            response = admin_client.get(url)
            assert response.status_code in [
                HTTP_200_OK,
                HTTP_302_FOUND,
                HTTP_403_FORBIDDEN,
            ], f"Add page failed for {app_label}.{model_name}"


@pytest.mark.django_db
def test_admin_change_pages(admin_client):
    """Test change/edit pages for existing objects"""
    for model in admin.site._registry:
        if hasattr(model, "objects"):
            first = model.objects.first()
            if first:
                app_label = model._meta.app_label
                model_name = model._meta.model_name

                url = reverse(f"admin:{app_label}_{model_name}_change", args=[first.pk])
                response = admin_client.get(url)
                assert response.status_code in [HTTP_200_OK, HTTP_302_FOUND], (
                    f"Change page failed for {app_label}.{model_name}"
                )


@pytest.mark.django_db
def test_admin_save_operations(admin_client, mock_request):
    """Test save/update operations (only if user has permission)"""
    for model, model_admin in admin.site._registry.items():
        if hasattr(model, "objects"):
            first = model.objects.first()
            if first and model_admin.has_change_permission(mock_request, first):
                app_label = model._meta.app_label
                model_name = model._meta.model_name

                url = reverse(f"admin:{app_label}_{model_name}_change", args=[first.pk])
                # First check if the page loads
                response = admin_client.get(url)
                if response.status_code == HTTP_200_OK:
                    try:
                        save_response = admin_client.post(
                            url, data={"_continue": "Save and continue editing"}
                        )
                        assert save_response.status_code in [
                            HTTP_200_OK,
                            HTTP_302_FOUND,
                        ], f"Save failed for {app_label}.{model_name}"
                    except Exception as e:
                        pytest.fail(
                            f"Save operation raised exception for {app_label}.{model_name}: {e}"
                        )


@pytest.mark.django_db
def test_admin_delete_pages(admin_client, mock_request):
    """Test delete pages (only if user has permission)"""
    for model, model_admin in admin.site._registry.items():
        if hasattr(model, "objects"):
            first = model.objects.first()
            if first and model_admin.has_delete_permission(mock_request, first):
                app_label = model._meta.app_label
                model_name = model._meta.model_name

                url = reverse(f"admin:{app_label}_{model_name}_delete", args=[first.pk])
                response = admin_client.get(url)
                assert response.status_code in [
                    HTTP_200_OK,
                    HTTP_302_FOUND,
                    HTTP_403_FORBIDDEN,
                ], f"Delete page failed for {app_label}.{model_name}"


@pytest.mark.django_db
def test_admin_history_pages(admin_client):
    """Test history pages for existing objects"""
    for model in admin.site._registry:
        if hasattr(model, "objects"):
            first = model.objects.first()
            if first:
                app_label = model._meta.app_label
                model_name = model._meta.model_name

                try:
                    url = reverse(
                        f"admin:{app_label}_{model_name}_history", args=[first.pk]
                    )
                    response = admin_client.get(url)
                    assert response.status_code in [HTTP_200_OK, HTTP_302_FOUND], (
                        f"History page failed for {app_label}.{model_name}"
                    )
                except Exception as e:
                    pytest.fail(
                        f"History page raised exception for {app_label}.{model_name}: {e}"
                    )
