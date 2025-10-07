"""
Explicit factory loader with full control over data creation.

Define exactly how many instances of each model and their relationships.
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


def load_all_factories(factor=1):
    """
    Load test data with explicit control over quantities and relationships.

    Args:
        factor: Multiplier for all quantities (e.g., factor=2 doubles everything)
    """
    # ========================================================================
    # SINGLETONS
    # ========================================================================
    if not AppInfoFactory._meta.model.objects.exists():
        AppInfoFactory.create()

    if not SocialAccountFactory._meta.model.objects.exists():
        SocialAccountFactory.create()

    # ========================================================================
    # INDEPENDENT MODELS
    # ========================================================================
    CountryFactory.create_batch(2 * factor)
    banner_groups = BannerGroupFactory.create_batch(3 * factor)
    FAQFactory.create_batch(5 * factor)
    OnboardingFactory.create_batch(3 * factor)
    popups = PopUpBannerFactory.create_batch(2 * factor)

    # ========================================================================
    # USER MODELS
    # ========================================================================
    AdminUserFactory.create_batch(2 * factor)
    customers = CustomerFactory.create_batch(5 * factor)  # Wallets auto-created

    # ========================================================================
    # DEPENDENT MODELS - EXPLICIT RELATIONSHIPS
    # ========================================================================

    # Create additional standalone wallets
    WalletFactory.create_batch(2 * factor)

    # Create 2 addresses per customer
    for customer in customers:
        AddressFactory.create_batch(2, customer=customer)

    # Create 1 contact per customer
    for customer in customers:
        ContactUsFactory.create(customer=customer)

    # Regions
    RegionFactory.create_batch(3 * factor)

    # Create 2 banners per group
    for group in banner_groups:
        BannerFactory.create_batch(2, group=group)

    # Notifications
    NotificationFactory.create_batch(3 * factor)

    # Create 1 popup tracking per customer per popup
    for customer in customers:
        for popup in popups:
            PopUpTrackingFactory.create(customer=customer, popup=popup)

    # Create 3 wallet transactions per customer
    for customer in customers:
        WalletTransactionFactory.create_batch(3, wallet=customer.wallet)
