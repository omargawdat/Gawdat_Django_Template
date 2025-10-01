"""
Test data coverage - ensure all models have test data
"""

import pytest
from django.contrib import admin


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
