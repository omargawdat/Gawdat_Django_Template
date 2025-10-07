"""
Test data coverage - ensure all models have test data

Validates that ALL Django models have test data loaded.
Fails if a new model is added without a corresponding factory.

This ensures comprehensive factory coverage for all models in the project.
"""

import pytest
from django.apps import apps


@pytest.mark.django_db
def test_all_models_have_test_data():
    """
    Check that ALL models have test data (factory coverage test).

    This iterates through all Django models in your apps/ directory
    and verifies each has at least one instance in the database.

    If a model has no data, you need to create a factory for it.
    """
    # Apps to check (your project apps)
    PROJECT_APPS = [
        "users",
        "location",
        "payment",
        "channel",
        "appInfo",
    ]

    # Models to ignore (third-party, built-in, or special cases)
    IGNORED_MODELS = {
        # Django built-in
        "auth.permission",
        "auth.group",
        "contenttypes.contenttype",
        "sessions.session",
        "admin.logentry",
        # Third-party packages
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
        # Simple History (auto-generated historical tables)
        # Add pattern matching for historical models
        # Your abstract models (if any)
        "users.user",  # Abstract base - Customer/AdminUser inherit from it
    }

    models_without_data = []
    checked_models = []

    # Get all models from project apps
    for app_name in PROJECT_APPS:
        try:
            app_models = apps.get_app_config(app_name).get_models()
        except LookupError:
            continue

        for model in app_models:
            # Skip if model doesn't have objects manager
            if not hasattr(model, "objects"):
                continue

            app_label = model._meta.app_label
            model_name = model._meta.model_name
            full_name = f"{app_label}.{model_name}"

            # Skip ignored models
            if full_name in IGNORED_MODELS:
                continue

            # Skip historical models (django-simple-history)
            if model_name.startswith("historical"):
                continue

            # Skip abstract models
            if model._meta.abstract:
                continue

            checked_models.append(full_name)

            # Check if model has data
            count = model.objects.count()
            if count == 0:
                models_without_data.append(full_name)

    # Build detailed error message
    if models_without_data:
        message = (
            f"\n{'=' * 70}\n"
            f"❌ FACTORY COVERAGE TEST FAILED\n"
            f"{'=' * 70}\n"
            f"\n{len(models_without_data)} model(s) have NO test data:\n\n"
        )

        for model_name in sorted(models_without_data):
            message += f"  ❌ {model_name}\n"

        message += (
            f"\n{'=' * 70}\n"
            f"📝 TO FIX:\n"
            f"{'=' * 70}\n"
            f"1. Create a factory for each missing model in factories/factories.py\n"
            f"2. Export it in factories/__init__.py\n"
            f"3. Re-run tests - data will be auto-loaded\n"
            f"\nExample:\n"
            f"  class MyModelFactory(factory.django.DjangoModelFactory):\n"
            f"      # ... field definitions ...\n"
            f"      class Meta:\n"
            f"          model = MyModel\n"
            f"\n{'=' * 70}\n"
            f"✅ Models with data: {len(checked_models) - len(models_without_data)}\n"
            f"❌ Models missing data: {len(models_without_data)}\n"
            f"📊 Total checked: {len(checked_models)}\n"
            f"{'=' * 70}\n"
        )

        pytest.fail(message)
