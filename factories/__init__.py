"""
Model Factories

This package contains Factory Boy factories for creating test data and seeding databases.
Factories can be used in:
- Tests (pytest fixtures)
- Development database seeding
- Management commands
- Data migration scripts

Usage:
    from factories import CustomerFactory, CountryFactory

    # Create a single instance
    customer = CustomerFactory()

    # Create multiple instances
    customers = CustomerFactory.create_batch(10)

    # Create with custom attributes
    customer = CustomerFactory(full_name="John Doe")

    # Use loader utilities
    from factories.loader import discover_factories, load_all_factories
"""

from factories.factories import AddressFactory
from factories.factories import AdminUserFactory
from factories.factories import AppInfoFactory
from factories.factories import BannerFactory
from factories.factories import BannerGroupFactory
from factories.factories import ContactUsFactory
from factories.factories import CountryFactory
from factories.factories import CustomerFactory
from factories.factories import FAQFactory
from factories.factories import NotificationFactory
from factories.factories import OnboardingFactory
from factories.factories import PopUpBannerFactory
from factories.factories import PopUpTrackingFactory
from factories.factories import RegionFactory
from factories.factories import SocialAccountFactory
from factories.factories import WalletFactory
from factories.factories import WalletTransactionFactory
from factories.loader import discover_factories
from factories.loader import load_all_factories

__all__ = [
    "AddressFactory",
    "AdminUserFactory",
    "AppInfoFactory",
    "BannerFactory",
    "BannerGroupFactory",
    "ContactUsFactory",
    "CountryFactory",
    "CustomerFactory",
    "FAQFactory",
    "NotificationFactory",
    "OnboardingFactory",
    "PopUpBannerFactory",
    "PopUpTrackingFactory",
    "RegionFactory",
    "SocialAccountFactory",
    "WalletFactory",
    "WalletTransactionFactory",
    "discover_factories",
    "load_all_factories",
]
