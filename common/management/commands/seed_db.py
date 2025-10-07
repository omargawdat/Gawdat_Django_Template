# management/commands/seed_db.py
import logging

from django.core.management.base import BaseCommand

from factories.loader import load_all_factories

# Configure logging to show INFO messages
logging.basicConfig(level=logging.INFO, format="%(message)s")


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
        if env.environment not in ("local", "development"):
            self.stdout.write(
                self.style.ERROR(
                    f"❌ seed_db only allowed in local/development, not '{env.environment}'"
                )
            )
            return

        factor = options["factor"]

        # Flush existing data if requested
        if options["flush"]:
            from django.core.management import call_command

            self.stdout.write(self.style.WARNING("\n🗑️  Flushing existing data...\n"))
            try:
                call_command("flush", "--no-input")
                self.stdout.write(self.style.SUCCESS("✓ Data flushed\n"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Flush failed: {e}"))
                self.stdout.write(self.style.WARNING("Continuing without flush...\n"))

            # Create superuser
            try:
                call_command("createsu")
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Could not create superuser: {e}")
                )

        # Seed database
        self.stdout.write(self.style.SUCCESS("🌱 Seeding database...\n"))
        load_all_factories(factor=factor)
        self.stdout.write(self.style.SUCCESS("\n✓ Database seeding complete!\n"))
