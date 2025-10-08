# management/commands/seed_db.py
import random

from django.core.management.base import BaseCommand

from factories.factories import AdminUserFactory
from factories.factories import AppInfoFactory
from factories.factories import BannerGroupFactory
from factories.factories import CountryFactory
from factories.factories import CustomerFactory
from factories.factories import FAQFactory
from factories.factories import NotificationFactory
from factories.factories import OnboardingFactory
from factories.factories import PaymentFactory
from factories.factories import PopUpBannerFactory
from factories.factories import PopUpTrackingFactory
from factories.factories import RegionFactory
from factories.factories import SocialAccountFactory


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
        """Load test data with relationships handled by factories."""
        # ========================================================================
        # SINGLETONS
        # ========================================================================
        AppInfoFactory.create()
        SocialAccountFactory.create()

        # ========================================================================
        # INDEPENDENT MODELS
        # ========================================================================
        CountryFactory.create_batch(2 * factor)
        BannerGroupFactory.create_batch(3 * factor)
        FAQFactory.create_batch(5 * factor)
        OnboardingFactory.create_batch(3 * factor)
        PopUpBannerFactory.create_batch(2 * factor)

        # ========================================================================
        # USER MODELS (auto-creates wallet, addresses, contact_us)
        # ========================================================================
        AdminUserFactory.create_batch(2 * factor)
        customers = CustomerFactory.create_batch(5 * factor)

        # ========================================================================
        # ADDITIONAL RELATIONSHIPS
        # ========================================================================

        # Regions
        RegionFactory.create_batch(3 * factor)

        # Notifications with M2M users
        notifications = NotificationFactory.create_batch(factor)
        for notification in notifications:
            notification.users.add(*random.sample(customers, k=min(3, len(customers))))

        # ========================================================================
        # DEPENDENT MODELS (require existing customers/banners)
        # ========================================================================

        # PopUp tracking for customers
        PopUpTrackingFactory.create_batch(2 * factor)

        # Payments for customers
        PaymentFactory.create_batch(3 * factor)
