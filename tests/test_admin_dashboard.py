"""
Simple admin test - loops through all admin models and checks if pages load
"""

import pytest
from django.contrib import admin
from django.test import Client
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
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.mark.django_db
def test_all_admin_pages(admin_client, admin_user, customer, banner):  # noqa: C901, PLR0912, PLR0915
    """Loop through all admin models and test if pages load"""

    passed = 0
    failed = 0

    # Test admin index
    response = admin_client.get(reverse("admin:index"))
    if response.status_code == HTTP_200_OK:
        passed += 1
    else:
        failed += 1

    # Create a mock request for permission checks
    from django.test import RequestFactory

    request_factory = RequestFactory()
    mock_request = request_factory.get("/admin/")
    mock_request.user = admin_user

    # Loop all admin models
    for model, model_admin in admin.site._registry.items():
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        # Test list page
        url = reverse(f"admin:{app_label}_{model_name}_changelist")
        response = admin_client.get(url)
        if response.status_code in [HTTP_200_OK, HTTP_302_FOUND]:
            passed += 1
        else:
            failed += 1

        # Test search functionality if search_fields is defined
        if hasattr(model_admin, "search_fields") and model_admin.search_fields:
            response = admin_client.get(url, {"q": "test"})
            if response.status_code == HTTP_200_OK:
                passed += 1
            else:
                failed += 1

        # Test add page (only if user has add permission)
        if model_admin.has_add_permission(mock_request):
            url = reverse(f"admin:{app_label}_{model_name}_add")
            response = admin_client.get(url)
            if response.status_code in [
                HTTP_200_OK,
                HTTP_302_FOUND,
                HTTP_403_FORBIDDEN,
            ]:
                passed += 1
            else:
                failed += 1

        # Test change/edit page if record exists
        if hasattr(model, "objects"):
            first = model.objects.first()
            if first:
                url = reverse(f"admin:{app_label}_{model_name}_change", args=[first.pk])
                response = admin_client.get(url)
                if response.status_code in [HTTP_200_OK, HTTP_302_FOUND]:
                    passed += 1
                else:
                    failed += 1

                # Test save/update (POST to change page, only if user has change permission)
                if (
                    response.status_code == HTTP_200_OK
                    and model_admin.has_change_permission(mock_request, first)
                ):
                    save_response = admin_client.post(
                        url, data={"_continue": "Save and continue editing"}
                    )
                    if save_response.status_code in [HTTP_200_OK, HTTP_302_FOUND]:
                        passed += 1
                    else:
                        failed += 1

                # Test delete page (only if user has delete permission)
                if model_admin.has_delete_permission(mock_request, first):
                    url = reverse(
                        f"admin:{app_label}_{model_name}_delete", args=[first.pk]
                    )
                    response = admin_client.get(url)
                    if response.status_code in [
                        HTTP_200_OK,
                        HTTP_302_FOUND,
                        HTTP_403_FORBIDDEN,
                    ]:
                        passed += 1

    assert failed == 0
