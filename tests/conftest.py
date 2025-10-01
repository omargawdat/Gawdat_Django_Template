"""
Register factories as pytest fixtures
"""

import inspect

import pytest
from djmoney.money import Money
from pytest_factoryboy import register

from tests import factories

# Automatically register all factories from factories module
REGISTERED_FACTORIES = []
for name, obj in inspect.getmembers(factories):
    if (
        inspect.isclass(obj)
        and name.endswith("Factory")
        and hasattr(obj, "_meta")
        and hasattr(obj._meta, "model")
    ):
        register(obj)
        # Store the fixture name (pytest_factoryboy converts FooFactory -> foo_factory)
        fixture_name = name.replace("Factory", "").lower() + "_factory"
        REGISTERED_FACTORIES.append(fixture_name)


@pytest.fixture(autouse=True)
def setup_test_data(request):
    """Automatically create test data for all registered factories"""
    for factory_name in REGISTERED_FACTORIES:
        try:
            factory = request.getfixturevalue(factory_name)
            if hasattr(factory, "create_batch"):
                factory.create_batch(2)
        except Exception:  # noqa: S110
            # Skip if factory is not available or fails
            # This is expected for some factories that may have dependencies
            pass


@pytest.fixture(scope="session", autouse=True)
def create_un_country(django_db_setup, django_db_blocker):
    """Create UN country required by WalletService"""
    with django_db_blocker.unblock():
        from io import BytesIO

        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image

        from apps.location.models.country import Country

        # Create a dummy flag image
        image = Image.new("RGB", (100, 100), color="gray")
        buffer = BytesIO()
        image.save(buffer, "PNG")
        buffer.seek(0)
        flag_file = SimpleUploadedFile(
            "un_flag.png", buffer.read(), content_type="image/png"
        )

        Country.objects.get_or_create(
            code="UN",
            defaults={
                "name": "Unselected",
                "currency": "USD",
                "flag": flag_file,
                "is_active": True,
                "phone_code": "000",
                "app_install_money_inviter": Money(0, "USD"),
                "app_install_money_invitee": Money(0, "USD"),
                "order_money_inviter": Money(0, "USD"),
                "order_money_invitee": Money(0, "USD"),
            },
        )
