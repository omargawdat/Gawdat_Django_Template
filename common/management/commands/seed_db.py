"""
Management command to seed database with factory data

Auto-discovers all factories and creates random amounts of data.

Usage:
    python manage.py seed_db                    # Random amounts (5-20 per model)
    python manage.py seed_db --count 50         # Fixed amount for all models
    python manage.py seed_db --min 10 --max 30 # Random between min-max
    python manage.py seed_db --flush            # Clear data first
"""

import inspect
import random

from django.core.management.base import BaseCommand
from django.db import transaction

import factories as factories_module


class Command(BaseCommand):
    help = "Seed database with test data using all available factories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            help="Fixed number of instances to create for each factory",
        )
        parser.add_argument(
            "--min",
            type=int,
            default=5,
            help="Minimum number of instances per factory (default: 5)",
        )
        parser.add_argument(
            "--max",
            type=int,
            default=20,
            help="Maximum number of instances per factory (default: 20)",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Flush existing data before seeding",
        )

    def _discover_factories(self):
        """Auto-discover all factories from factories module (same as tests/conftest.py)"""
        discovered_factories = []

        for name, obj in inspect.getmembers(factories_module):
            if (
                inspect.isclass(obj)
                and name.endswith("Factory")
                and hasattr(obj, "_meta")
                and hasattr(obj._meta, "model")
            ):
                discovered_factories.append((name, obj))

        return discovered_factories

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write(self.style.WARNING("Flushing existing data..."))
            self._flush_data()

        # Auto-discover all factories
        factories = self._discover_factories()

        if not factories:
            self.stdout.write(self.style.ERROR("No factories found!"))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Discovered {len(factories)} factories. Seeding database...\n"
            )
        )

        total_created = 0
        created_summary = []

        # Create data for each factory
        for _, factory_class in factories:
            # Determine count for this factory
            if options["count"]:
                count = options["count"]
            else:
                count = random.randint(options["min"], options["max"])  # noqa: S311

            model_name = factory_class._meta.model.__name__

            try:
                self.stdout.write(f"  Creating {count} {model_name}(s)...")
                factory_class.create_batch(count)
                total_created += count
                created_summary.append(f"  - {count} {model_name}(s)")
                self.stdout.write(
                    self.style.SUCCESS(f"    ✓ Created {count} {model_name}(s)")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"    ⚠ Skipped {model_name}: {e!s}")
                )

        # Print summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Database seeded successfully!\n"
                f"Total instances created: {total_created}\n\n"
                + "\n".join(created_summary)
            )
        )

    def _flush_data(self):
        """Flush existing factory-created data by auto-discovering models"""
        from django.db.models.deletion import ProtectedError

        factories = self._discover_factories()

        # Collect all models from factories
        models_to_flush = []
        for _, factory_class in factories:
            model = factory_class._meta.model
            models_to_flush.append((model.__name__, model))

        # Delete in reverse order (to handle dependencies)
        for model_name, model in reversed(models_to_flush):
            try:
                # Special handling for Country - keep UN country
                if model_name == "Country":
                    count = model.objects.exclude(code="UN").count()
                    model.objects.exclude(code="UN").delete()
                    self.stdout.write(
                        f"    Deleted {count} {model_name}(s) (kept UN country)"
                    )
                else:
                    count = model.objects.count()
                    model.objects.all().delete()
                    self.stdout.write(f"    Deleted {count} {model_name}(s)")
            except ProtectedError:
                self.stdout.write(
                    self.style.WARNING(
                        f"    ⚠ Cannot delete {model_name}: protected by foreign keys"
                    )
                )

        self.stdout.write(self.style.SUCCESS("✓ Data flushed"))
