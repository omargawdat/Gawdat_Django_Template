# management/commands/seed_db.py
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from factories import AddressFactory
from factories import AdminUserFactory
from factories import AppInfoFactory
from factories import BannerFactory
from factories import BannerGroupFactory
from factories import ContactUsFactory
from factories import CountryFactory
from factories import CustomerFactory
from factories import FAQFactory
from factories import NotificationFactory
from factories import OnboardingFactory
from factories import PopUpBannerFactory
from factories import RegionFactory
from factories import SocialAccountFactory
from factories import WalletFactory
from factories import WalletTransactionFactory

# Single source of truth for factory ordering
# Order matters: dependencies must come after their dependents
FACTORY_REGISTRY = [
    # Independent models (no foreign keys)
    {"factory": CountryFactory, "count": len(settings.SUPPORTED_COUNTRY_CODES)},
    {"factory": AppInfoFactory, "count": 1},
    {"factory": SocialAccountFactory, "count": 1},
    # User models
    {"factory": AdminUserFactory, "count": "count"},
    {"factory": CustomerFactory, "count": "count"},  # Auto-creates wallets
    # Customer-dependent models
    {"factory": AddressFactory, "count": "1.5x"},
    {"factory": ContactUsFactory, "count": "0.8x"},
    # Content models
    {"factory": BannerGroupFactory, "count": 10},
    {"factory": BannerFactory, "count": "count"},
    {"factory": FAQFactory, "count": 15},
    {"factory": OnboardingFactory, "count": "count"},
    {"factory": PopUpBannerFactory, "count": "count"},
    # Location models
    {"factory": RegionFactory, "count": "count"},
    # Transaction models
    {"factory": NotificationFactory, "count": "count"},
    {"factory": WalletTransactionFactory, "count": "count"},
]


class Command(BaseCommand):
    help = "Seed database with test data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="Number of instances to create (default: 20)",
        )
        parser.add_argument(
            "--no-flush",
            action="store_false",
            dest="flush",
            default=True,
            help="Skip flushing data",
        )

    def handle(self, *args, **options):
        from config.helpers.env import env

        if env.environment not in ("local", "development"):
            self.stdout.write(
                self.style.ERROR(
                    f"❌ seed_db only allowed in local/development, not '{env.environment}'"
                )
            )
            return

        count = options["count"]

        if options["flush"]:
            self.stdout.write(self.style.WARNING("Flushing existing data..."))
            self._flush_data()

            from django.core.management import call_command

            call_command("createsu")

        self.stdout.write(self.style.SUCCESS("\n🌱 Seeding database...\n"))

        total_created = 0
        created_summary = []

        for config in FACTORY_REGISTRY:
            factory_class = config["factory"]
            count_spec = config["count"]
            kwargs = config.get("kwargs", {})

            # Calculate actual count from specification
            create_count = self._calculate_count(count_spec, count)

            # Get model name from factory
            model_name = factory_class._meta.model.__name__

            try:
                self.stdout.write(f"  Creating {create_count} {model_name}(s)...")

                with transaction.atomic():
                    if create_count == 1:
                        factory_class.create(**kwargs)
                        actual_count = 1
                    else:
                        factory_class.create_batch(create_count, **kwargs)
                        actual_count = create_count

                    total_created += actual_count
                    created_summary.append(f"  ✓ {actual_count} {model_name}(s)")
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"    ✓ Created {actual_count} {model_name}(s)"
                        )
                    )

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"    ✗ Failed {model_name}: {e}"))

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Database seeded successfully!\n"
                f"Total instances: {total_created}\n\n" + "\n".join(created_summary)
            )
        )

    def _flush_data(self):
        """Flush data in reverse dependency order"""
        from django.db.models.deletion import ProtectedError

        # Reverse registry order + add WalletFactory (auto-created)
        factories_to_flush = [
            config["factory"] for config in reversed(FACTORY_REGISTRY)
        ]
        # Add WalletFactory since it's auto-created but not in registry
        factories_to_flush.insert(0, WalletFactory)

        for factory_class in factories_to_flush:
            model = factory_class._meta.model
            model_name = model.__name__

            try:
                count = model.objects.count()
                model.objects.all().delete()
                self.stdout.write(f"    Deleted {count} {model_name}(s)")
            except ProtectedError:
                self.stdout.write(
                    self.style.WARNING(f"    ⚠ Cannot delete {model_name}: protected")
                )

        self.stdout.write(self.style.SUCCESS("✓ Data flushed"))

    def _calculate_count(self, count_spec, base_count):
        """
        Calculate actual count from specification

        Args:
            count_spec: Can be:
                - int: exact count
                - "count": use base_count
                - "1.5x", "0.8x": multiply base_count
            base_count: Base count from command argument

        Returns:
            int: Calculated count
        """
        if isinstance(count_spec, int):
            return count_spec

        if count_spec == "count":
            return base_count

        if isinstance(count_spec, str) and count_spec.endswith("x"):
            multiplier = float(count_spec[:-1])
            return int(base_count * multiplier)

        return base_count
