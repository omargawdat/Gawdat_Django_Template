"""
Test admin CRUD operations (save, delete)

Test data is automatically loaded via session-scoped fixture in conftest.py.
"""

import pytest
from django.contrib import admin
from django.urls import reverse

HTTP_200_OK = 200
HTTP_302_FOUND = 302
HTTP_403_FORBIDDEN = 403


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
