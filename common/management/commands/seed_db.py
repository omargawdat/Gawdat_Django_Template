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
            "--count",
            type=int,
            default=20,
            help="Base number of instances to create (default: 20)",
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

        count = options["count"]

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

        # Seed database using unified loader
        self.stdout.write(self.style.SUCCESS("🌱 Seeding database...\n"))

        stats = load_all_factories(count=count, verbose=True)

        # Summary
        total = stats["success"] + stats["failed"] + stats["skipped"]
        self.stdout.write(
            self.style.SUCCESS(
                f"\n{'=' * 60}\n"
                f"✓ Database seeding complete!\n"
                f"{'=' * 60}\n"
                f"  Success: {stats['success']}\n"
                f"  Failed:  {stats['failed']}\n"
                f"  Skipped: {stats['skipped']}\n"
                f"  Total:   {total}\n"
                f"{'=' * 60}\n"
            )
        )
