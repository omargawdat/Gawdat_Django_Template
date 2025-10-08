"""
Test factory coverage - ensure all models have factories.

Strategy:
1. Session fixture loads all factories (conftest.py)
2. This test just checks which models have no data
3. Reports missing factories
"""

import pytest
from django.apps import apps


@pytest.mark.django_db
def test_all_models_have_factories():
    """
    Check which models have no data after factory loading.

    This validates that all project models have corresponding factories.
    Data is already loaded by session fixture in conftest.py.
    """
    # Models to ignore (third-party, built-in, abstract)
    IGNORED_MODELS = {
        # Django built-in
        "auth.permission",
        "auth.group",
        "contenttypes.contenttype",
        "sessions.session",
        "admin.logentry",
        # Third-party
        "constance.constance",
        "fcm_django.fcmdevice",
        "authtoken.token",
        "authtoken.tokenproxy",
        "token_blacklist.outstandingtoken",
        "token_blacklist.blacklistedtoken",
        "account.emailaddress",
        "account.emailconfirmation",
        "socialaccount.socialapp",
        "socialaccount.socialtoken",
        "socialaccount.socialaccount",
        "sites.site",
        # apps
        # ignore PopUpTrackingFactory
        "appinfo.popuptracking",
    }

    # Check which models have no data
    models_without_data = []

    # Iterate through ALL installed apps and models
    for model in apps.get_models():
        if not hasattr(model, "objects"):
            continue

        app_label = model._meta.app_label
        model_name = model._meta.model_name
        full_name = f"{app_label}.{model_name}"

        # Skip ignored/abstract/historical models
        if (
            full_name in IGNORED_MODELS
            or model_name.startswith("historical")
            or model._meta.abstract
        ):
            continue

        # Check if model has data
        if model.objects.count() == 0:
            models_without_data.append(full_name)

    # Report results
    if models_without_data:
        message = (
            f"\n{'=' * 70}\n"
            f"❌ FACTORY COVERAGE TEST FAILED\n"
            f"{'=' * 70}\n"
            f"\n{len(models_without_data)} model(s) missing factories:\n\n"
        )

        for model_name in sorted(models_without_data):
            message += f"  ❌ {model_name}\n"

        message += (
            f"\n{'=' * 70}\n"
            f"📝 TO FIX: Create factories in factories/factories.py\n"
            f"{'=' * 70}\n"
        )

        pytest.fail(message)
