"""
Test admin page loading and navigation
"""

import pytest
from django.contrib import admin
from django.urls import reverse

from factories.loader import load_all_factories

HTTP_200_OK = 200
HTTP_302_FOUND = 302


@pytest.mark.django_db
class TestAdminPages:
    """Test admin pages with test data"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_test_data(self, django_db_blocker):
        """Create test data once for all tests in this class"""
        with django_db_blocker.unblock():
            load_all_factories(count=2, use_transaction=False)

    def test_admin_index(self, admin_client):
        """Test admin index page loads"""
        response = admin_client.get(reverse("admin:index"))
        assert response.status_code == HTTP_200_OK

    def test_admin_list_pages(self, admin_client):
        """Test all admin changelist pages load"""
        for model in admin.site._registry:
            app_label = model._meta.app_label
            model_name = model._meta.model_name

            url = reverse(f"admin:{app_label}_{model_name}_changelist")
            response = admin_client.get(url)
            assert response.status_code in [HTTP_200_OK, HTTP_302_FOUND], (
                f"List page failed for {app_label}.{model_name}"
            )

    def test_admin_search(self, admin_client):
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

    def test_admin_add_pages(self, admin_client, mock_request):
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
                ], f"Add page failed for {app_label}.{model_name}"

    def test_admin_change_pages(self, admin_client):
        """Test change/edit pages for existing objects"""
        for model in admin.site._registry:
            if hasattr(model, "objects"):
                first = model.objects.first()
                if first:
                    app_label = model._meta.app_label
                    model_name = model._meta.model_name

                    url = reverse(
                        f"admin:{app_label}_{model_name}_change", args=[first.pk]
                    )
                    response = admin_client.get(url)
                    assert response.status_code in [HTTP_200_OK, HTTP_302_FOUND], (
                        f"Change page failed for {app_label}.{model_name}"
                    )

    def test_admin_history_pages(self, admin_client):
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

    def test_admin_list_sorting(self, admin_client, mock_request):
        """Test sorting by each column in list_display"""
        sorting_failures = []

        for model, model_admin in admin.site._registry.items():
            # Skip if no data exists
            if not hasattr(model, "objects") or model.objects.count() == 0:
                continue

            app_label = model._meta.app_label
            model_name = model._meta.model_name

            # Get list_display fields
            list_display = model_admin.get_list_display(mock_request)
            if not list_display:
                continue

            base_url = reverse(f"admin:{app_label}_{model_name}_changelist")

            # Test sorting by each column (ascending and descending)
            for idx in range(len(list_display)):
                field_name = list_display[idx]

                # Test ascending sort
                try:
                    response = admin_client.get(base_url, {"o": str(idx)})
                    if response.status_code != HTTP_200_OK:
                        sorting_failures.append(
                            f"{app_label}.{model_name} column {idx} ({field_name}): "
                            f"Status {response.status_code} (ascending)"
                        )
                except Exception as e:
                    error_msg = str(e).split("\n")[0] if "\n" in str(e) else str(e)
                    sorting_failures.append(
                        f"{app_label}.{model_name} column {idx} ({field_name}): "
                        f"{error_msg} (ascending)"
                    )

                # Test descending sort
                try:
                    response = admin_client.get(base_url, {"o": f"-{idx}"})
                    if response.status_code != HTTP_200_OK:
                        sorting_failures.append(
                            f"{app_label}.{model_name} column {idx} ({field_name}): "
                            f"Status {response.status_code} (descending)"
                        )
                except Exception as e:
                    error_msg = str(e).split("\n")[0] if "\n" in str(e) else str(e)
                    sorting_failures.append(
                        f"{app_label}.{model_name} column {idx} ({field_name}): "
                        f"{error_msg} (descending)"
                    )

        # Report all failures at once
        if sorting_failures:
            failure_message = (
                f"\n\n{'=' * 70}\n"
                f"Sorting failures found in {len(sorting_failures)} column(s):\n"
                f"{'=' * 70}\n"
            )
            for failure in sorting_failures:
                failure_message += f"  ❌ {failure}\n"
            pytest.fail(failure_message)
