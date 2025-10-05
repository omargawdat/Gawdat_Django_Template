# management/commands/seed_db.py
from django.core.management.base import BaseCommand
from django.db import transaction

from factories.loader import discover_factories
from factories.loader import get_factory_priority
from factories.loader import get_factory_seed_count


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
            from django.core.management import call_command

            self.stdout.write(self.style.WARNING("Flushing existing data..."))
            call_command("flush", "--no-input")
            self.stdout.write(self.style.SUCCESS("✓ Data flushed"))

            call_command("createsu")

        self.stdout.write(self.style.SUCCESS("\n🌱 Seeding database...\n"))

        # Auto-discover all factories and sort by priority
        all_factories = discover_factories()
        sorted_factories = sorted(
            all_factories, key=lambda x: get_factory_priority(x[1])
        )

        total_created = 0
        created_summary = []

        for _factory_name, factory_class in sorted_factories:
            model = factory_class._meta.model
            model_name = model.__name__

            # Skip singletons if they already exist
            if hasattr(model, "singleton_instance_id"):
                if model.objects.exists():
                    self.stdout.write(
                        self.style.WARNING(
                            f"  ⊘ Skipping {model_name} (singleton already exists)"
                        )
                    )
                    continue

            # Get count specification from factory config
            count_spec = get_factory_seed_count(factory_class, count)

            # Calculate actual count from specification
            create_count = self._calculate_count(count_spec, count)

            try:
                self.stdout.write(f"  Creating {create_count} {model_name}(s)...")

                with transaction.atomic():
                    if create_count == 1:
                        factory_class.create()
                        actual_count = 1
                    else:
                        factory_class.create_batch(create_count)
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
