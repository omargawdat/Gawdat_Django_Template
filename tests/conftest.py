"""
Pytest fixtures for automatic test data setup

Auto-discovers all factories and creates test data before each test.
Data is automatically cleaned up via Django's transaction rollback.
"""

import inspect

import pytest
from djmoney.money import Money
from pytest_factoryboy import register

import factories as factories_module
from factories.loader import load_all_factories

# Auto-register all factories as pytest fixtures
for name, obj in inspect.getmembers(factories_module):
    if (
        inspect.isclass(obj)
        and name.endswith("Factory")
        and hasattr(obj, "_meta")
        and hasattr(obj._meta, "model")
    ):
        register(obj)


@pytest.fixture(autouse=True)
def setup_test_data(db, django_db_reset_sequences):
    """Create test data for all factories before each test"""
    load_all_factories(count=2, use_transaction=False)


@pytest.fixture(autouse=True)
def create_un_country(db):
    """Create UN country required by WalletService"""
    from io import BytesIO

    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image

    from apps.location.models.country import Country

    image = Image.new("RGB", (100, 100), color="gray")
    buffer = BytesIO()
    image.save(buffer, "PNG")
    buffer.seek(0)

    Country.objects.get_or_create(
        code="UN",
        defaults={
            "name": "Unselected",
            "currency": "USD",
            "flag": SimpleUploadedFile("un.png", buffer.read(), "image/png"),
            "is_active": True,
            "phone_code": "000",
            "app_install_money_inviter": Money(0, "USD"),
            "app_install_money_invitee": Money(0, "USD"),
            "order_money_inviter": Money(0, "USD"),
            "order_money_invitee": Money(0, "USD"),
        },
    )
