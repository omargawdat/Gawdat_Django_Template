# management/commands/seed_db.py
import random
import time
from contextlib import contextmanager

from django.core.management.base import BaseCommand
from django.db import connection

from apps.appInfo.models.banner import Banner
from apps.appInfo.models.banner_group import BannerGroup
from factories.factories import AdminUserFactory
from factories.factories import AppInfoFactory
from factories.factories import BannerFactory
from factories.factories import BannerGroupFactory
from factories.factories import CountryFactory
from factories.factories import CustomerFactory
from factories.factories import FAQFactory
from factories.factories import NotificationFactory
from factories.factories import OnboardingFactory
from factories.factories import PaymentFactory
from factories.factories import PopUpBannerFactory
from factories.factories import RegionFactory
from factories.factories import SocialAccountFactory


class Command(BaseCommand):
    help = "Seed database with test data using factories"

    @contextmanager
    def _timer(self, label):
        """Context manager to time operations and print debug info."""
        start_time = time.time()
        start_queries = len(connection.queries)

        self.stdout.write(f"⏳ {label}...")

        yield

        elapsed = time.time() - start_time
        num_queries = len(connection.queries) - start_queries
        self.stdout.write(
            self.style.SUCCESS(f"✓ {label} - {elapsed:.2f}s ({num_queries} queries)")
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            required=True,
            help="Base count for data quantities",
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

        count = options["count"]
        total_start = time.time()

        # Flush existing data if requested
        if options["flush"]:
            from django.core.management import call_command

            with self._timer("Flushing database"):
                call_command("flush", "--no-input", verbosity=0)
                call_command("createsu", verbosity=0)

        # Seed database
        self._load_all_factories(count)

        # Output summary
        total_elapsed = time.time() - total_start
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Seeded (count={count}) - Total time: {total_elapsed:.2f}s"
            )
        )

    def _load_all_factories(self, count):
        fixed_count = 10
        """Load test data with relationships handled by factories."""
        # ========================================================================
        # SINGLETONS
        # ========================================================================
        with self._timer("Creating singletons (AppInfo, SocialAccount)"):
            AppInfoFactory.create()
            SocialAccountFactory.create()

        # ========================================================================
        # INDEPENDENT MODELS
        # ========================================================================
        # TODO: Use bulk create for countries (requires handling LazyAttribute for Money fields)
        with self._timer(f"Creating {fixed_count} countries"):
            CountryFactory.create_batch(fixed_count)

        with self._timer(f"Creating {count} banner groups + banners (bulk)"):
            # Create banner groups in bulk
            groups = [BannerGroupFactory.build() for _ in range(count)]
            banner_groups = BannerGroup.objects.bulk_create(groups)

            # Create 2 banners per group in bulk
            banners = []
            for group in banner_groups:
                banners.extend([BannerFactory.build(group=group) for _ in range(2)])
            Banner.objects.bulk_create(banners)

        with self._timer(f"Creating {count} FAQs (bulk)"):
            FAQFactory.create_batch_bulk(count)

        with self._timer(f"Creating {count} onboarding screens (bulk)"):
            OnboardingFactory.create_batch_bulk(count)

        with self._timer(f"Creating {count} popup banners (bulk)"):
            PopUpBannerFactory.create_batch_bulk(count)

        # ========================================================================
        # USER MODELS (auto-creates wallet, addresses, contact_us)
        # ========================================================================
        # TODO: Cannot use bulk - AdminUser uses multi-table inheritance (polymorphic)
        with self._timer(f"Creating {fixed_count} admin users"):
            AdminUserFactory.create_batch(fixed_count)

        # TODO: Cannot use bulk - Customer has post_generation hooks (wallet, addresses, contact_us)
        with self._timer(
            f"Creating {count} customers (+ wallets, addresses, contact_us)"
        ):
            customers = CustomerFactory.create_batch(fixed_count)

        # ========================================================================
        # ADDITIONAL RELATIONSHIPS
        # ========================================================================
        with self._timer(f"Creating {count} regions (bulk)"):
            RegionFactory.create_batch_bulk(count)

        with self._timer(f"Creating {fixed_count} notifications with M2M users (bulk)"):
            notifications = NotificationFactory.create_batch_bulk(fixed_count)
            # Get User instances from customers for notifications
            customer_users = [customer.user for customer in customers]
            for notification in notifications:
                # Randomly assign users to each notification
                selected_users = random.sample(
                    customer_users, k=min(3, len(customer_users))
                )
                notification.users.add(*selected_users)

        # ========================================================================
        # PAYMENT MODELS
        # ========================================================================
        with self._timer(f"Creating {count} payments (bulk)"):
            PaymentFactory.create_batch_bulk(count, customers=customers)
