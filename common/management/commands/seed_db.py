# management/commands/seed_db.py
from django.core.management.base import BaseCommand

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


class Command(BaseCommand):
    help = "Seed database with test data using factories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--factor",
            type=int,
            default=4,
            help="Multiplier for data quantities (default: 4)",
        )
        parser.add_argument(
            "--no-flush",
            action="store_false",
            dest="flush",
            default=True,
            help="Skip flushing data before seeding",
        )

    def handle(self, *args, **options):
        from config.helpers.env import env

        # Safety check: only allow in development
        if env.environment not in ("local", "development", "test"):
            self.stdout.write(
                self.style.ERROR(
                    f"❌ seed_db only allowed in local/development/test, not '{env.environment}'"
                )
            )
            return

        factor = options["factor"]

        # Flush existing data if requested
        if options["flush"]:
            from django.core.management import call_command

            call_command("flush", "--no-input", verbosity=0)
            call_command("createsu", verbosity=0)

        # Seed database
        self._load_all_factories(factor)

        # Output summary
        self.stdout.write(self.style.SUCCESS(f"✓ Seeded (factor={factor})"))

    def _load_all_factories(self, factor):
        """Load test data with explicit control over quantities and relationships."""
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

        # Create banner groups with explicit order
        banner_groups = [BannerGroupFactory.create(order=i) for i in range(3 * factor)]

        # Create FAQs with explicit order
        for i in range(5 * factor):
            FAQFactory.create(order=i)

        # Create onboarding screens with explicit order
        for i in range(3 * factor):
            OnboardingFactory.create(order=i)

        popups = PopUpBannerFactory.create_batch(2 * factor)

        # ========================================================================
        # USER MODELS
        # ========================================================================
        AdminUserFactory.create_batch(2 * factor)
        customers = CustomerFactory.create_batch(5)  # Fixed number for customers

        # ========================================================================
        # DEPENDENT MODELS - EXPLICIT RELATIONSHIPS
        # ========================================================================

        # Single loop: Create all customer-related objects
        for customer in customers:
            # 1. Create wallet first (required for transactions)
            wallet = WalletFactory.create(user=customer)

            # 2. Create customer-related data
            AddressFactory.create_batch(2, customer=customer)
            ContactUsFactory.create(customer=customer)

            # 3. Create popup tracking for each popup
            for popup in popups:
                PopUpTrackingFactory.create(customer=customer, popup=popup)

            # 4. Create wallet transactions (after wallet exists)
            WalletTransactionFactory.create_batch(3, wallet=wallet)

        # Additional standalone wallets
        WalletFactory.create_batch(2 * factor)

        # Regions
        RegionFactory.create_batch(3 * factor)

        # Single loop: Create banners for each group
        for group in banner_groups:
            BannerFactory.create_batch(2, group=group)

        # Notifications with users
        notifications = NotificationFactory.create_batch(3 * factor)
        for notification in notifications:
            notification.users.add(*customers[:3])
