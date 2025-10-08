# management/commands/seed_db.py
import random
import time
from contextlib import contextmanager

from django.core.management.base import BaseCommand
from django.db import connection

from factories.factories import AdminUserFactory
from factories.factories import AppInfoFactory
from factories.factories import BannerGroupFactory
from factories.factories import CountryFactory
from factories.factories import CustomerFactory
from factories.factories import FAQFactory
from factories.factories import NotificationFactory
from factories.factories import OnboardingFactory
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
        total_start = time.time()

        # Flush existing data if requested
        if options["flush"]:
            from django.core.management import call_command

            with self._timer("Flushing database"):
                call_command("flush", "--no-input", verbosity=0)
                call_command("createsu", verbosity=0)

        # Seed database
        self._load_all_factories(factor)

        # Output summary
        total_elapsed = time.time() - total_start
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Seeded (factor={factor}) - Total time: {total_elapsed:.2f}s"
            )
        )

    def _load_all_factories(self, factor):
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
        with self._timer(f"Creating {2 * factor} countries"):
            CountryFactory.create_batch(2 * factor)

        # TODO: Use bulk create for banner groups (requires handling post_generation banners)
        with self._timer(f"Creating {3 * factor} banner groups"):
            BannerGroupFactory.create_batch(3 * factor)

        with self._timer(f"Creating {5 * factor} FAQs (bulk)"):
            FAQFactory.create_batch_bulk(5 * factor)

        with self._timer(f"Creating {3 * factor} onboarding screens (bulk)"):
            OnboardingFactory.create_batch_bulk(3 * factor)

        with self._timer(f"Creating {2 * factor} popup banners (bulk)"):
            PopUpBannerFactory.create_batch_bulk(2 * factor)

        # ========================================================================
        # USER MODELS (auto-creates wallet, addresses, contact_us)
        # ========================================================================
        # TODO: Cannot use bulk - AdminUser uses multi-table inheritance (polymorphic)
        with self._timer(f"Creating {2 * factor} admin users"):
            AdminUserFactory.create_batch(2 * factor)

        # TODO: Cannot use bulk - Customer has post_generation hooks (wallet, addresses, contact_us)
        with self._timer(
            f"Creating {5 * factor} customers (+ wallets, addresses, contact_us)"
        ):
            customers = CustomerFactory.create_batch(5 * factor)

        # ========================================================================
        # ADDITIONAL RELATIONSHIPS
        # ========================================================================
        with self._timer(f"Creating {3 * factor} regions (bulk)"):
            RegionFactory.create_batch_bulk(3 * factor)

        with self._timer(f"Creating {factor} notifications with M2M users (bulk)"):
            notifications = NotificationFactory.create_batch_bulk(factor)
            for notification in notifications:
                notification.users.add(
                    *random.sample(customers, k=min(3, len(customers)))
                )
