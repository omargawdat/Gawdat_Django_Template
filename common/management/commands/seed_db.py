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
