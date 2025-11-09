"""Test UNFOLD sidebar permissions match admin URLs."""

import inspect
import re

import pytest
from django.apps import apps

from config.integrations.unfold import UNFOLD


class TestUnfoldSidebarPermissions:
    """Validate UNFOLD sidebar permissions are correct."""

    @pytest.mark.django_db
    def test_sidebar_permissions_match_admin_urls(self):
        """Each sidebar permission should match its admin URL."""
        navigation = UNFOLD.get("SIDEBAR", {}).get("navigation", [])

        for section in navigation:
            section_title = str(section.get("title", ""))

            for item in section.get("items", []):
                if "permission" not in item or "link" not in item:
                    continue

                item_title = str(item["title"])
                admin_url = str(item["link"])
                permission_lambda = item["permission"]

                # Extract app and model from admin URL
                # URL can be either pattern "admin:app_model_changelist" or resolved "/admin/app/model/"
                url_match = re.search(r"admin:(\w+)_(\w+)_changelist", admin_url)
                if not url_match:
                    # Try to parse resolved URL like "/admin/app/model/"
                    url_match = re.search(r"/admin/(\w+)/(\w+)/?", admin_url)

                assert url_match, (
                    f"[{section_title}] {item_title}: "
                    f"Could not parse admin URL: {admin_url}"
                )

                url_app = url_match.group(1)
                url_model = url_match.group(2)

                # Extract permission string from lambda
                permission_str = None
                try:
                    source = inspect.getsource(permission_lambda)
                    perm_match = re.search(r'["\']([\w]+\.view_[\w]+)["\']', source)
                    if perm_match:
                        permission_str = perm_match.group(1)
                except (OSError, TypeError):
                    # Fallback: check bytecode constants
                    if hasattr(permission_lambda, "__code__"):
                        for const in permission_lambda.__code__.co_consts:
                            if isinstance(const, str) and ".view_" in const:
                                permission_str = const
                                break

                assert permission_str, (
                    f"[{section_title}] {item_title}: "
                    f"Could not extract permission from lambda"
                )

                # Verify the model exists and get correct permission
                try:
                    model = apps.get_model(url_app, url_model)
                    expected_permission = (
                        f"{model._meta.app_label}.view_{model._meta.model_name}"
                    )
                except LookupError:
                    expected_permission = f"{url_app}.view_{url_model}"

                # Assert permission matches
                assert permission_str == expected_permission, (
                    f"[{section_title}] {item_title}:\n"
                    f"  URL:        admin:{url_app}_{url_model}_changelist\n"
                    f"  Permission: {permission_str}\n"
                    f"  Expected:   {expected_permission}"
                )
