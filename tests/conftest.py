"""
Register factories as pytest fixtures
"""

import pytest
from djmoney.money import Money
from pytest_factoryboy import register

from tests.factories import BannerFactory
from tests.factories import BannerGroupFactory
from tests.factories import CountryFactory
from tests.factories import CustomerFactory

register(CountryFactory)
register(CustomerFactory)
register(BannerGroupFactory)
register(BannerFactory)


@pytest.fixture(autouse=True)
def setup_test_data(country_factory, customer_factory, banner_factory):
    """Automatically create test data for all tests"""
    # Create test objects that admin tests will use
    country_factory.create_batch(2)
    customer_factory.create_batch(3)
    banner_factory.create_batch(2)


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
