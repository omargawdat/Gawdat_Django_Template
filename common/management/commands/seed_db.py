"""
Management command to seed database with factory data

Auto-discovers all factories and creates random amounts of data.
Flushes existing data by default.

Usage:
    python manage.py seed_db                    # Flush + Random amounts (5-20 per model)
    python manage.py seed_db --count 50         # Flush + Fixed amount for all models
    python manage.py seed_db --no-flush         # Don't flush, just add data
"""

import random

from django.core.management.base import BaseCommand
from django.db import transaction

from factories.loader import create_factory_data
from factories.loader import discover_factories


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
            "--no-flush",
            action="store_false",
            dest="flush",
            default=True,
            help="Skip flushing data (flush is enabled by default)",
        )

    def handle(self, *args, **options):
        from config.helpers.env import env

        # Safety check: only allow in local/development environments
        if env.environment not in ("local", "development"):
            self.stdout.write(
                self.style.ERROR(
                    f"❌ seed_db command is not allowed in '{env.environment}' environment.\n"
                    f"This command can only be run in 'local' or 'development' environments."
                )
            )
            return

        if options["flush"]:
            self.stdout.write(self.style.WARNING("Flushing existing data..."))
            self._flush_data()

            # Recreate superuser after flushing
            self.stdout.write(self.style.WARNING("\nRecreating superuser..."))
            from django.core.management import call_command

            call_command("createsu")

        # Auto-discover all factories
        factories = discover_factories()

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

        # Create data for each factory in separate transactions
        for _, factory_class in factories:
            # Determine count for this factory
            if options["count"]:
                count = options["count"]
            else:
                count = random.randint(options["min"], options["max"])  # noqa: S311

            model_name = factory_class._meta.model.__name__

            # Handle singleton models
            if hasattr(factory_class._meta.model, "singleton_instance_id"):
                count = 1

            try:
                self.stdout.write(f"  Creating {count} {model_name}(s)...")
                # Each factory creation in its own transaction
                with transaction.atomic():
                    success = create_factory_data(
                        factory_class, count, skip_if_exists=True
                    )

                    if success:
                        total_created += count
                        created_summary.append(f"  - {count} {model_name}(s)")
                        self.stdout.write(
                            self.style.SUCCESS(f"    ✓ Created {count} {model_name}(s)")
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"    ⚠ Skipped {model_name}: singleton already exists"
                            )
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

        factories = discover_factories()

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
