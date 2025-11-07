import logging
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save

logger = logging.getLogger(__name__)

# Verbosity level threshold for detailed output
VERBOSE_LEVEL = 2


class Command(BaseCommand):
    help = "Load JSON fixtures from the 'assets/fixtures' directory."

    def add_arguments(self, parser):
        parser.add_argument(
            "--continue-on-error",
            action="store_true",
            help="Continue loading remaining fixtures even if one fails (default: exit on first error)",
        )

    def handle(self, *args, **options):  # noqa: PLR0912, PLR0915
        fixtures_root_path = "assets/fixtures"
        continue_on_error = options.get("continue_on_error", False)
        verbosity = options.get("verbosity", 1)

        if not Path(fixtures_root_path).exists():
            error_msg = 'The "fixtures" folder does not exist at the project root.'
            logger.error(error_msg)
            self.stdout.write(self.style.ERROR(error_msg))
            return

        # Track results
        results = {"success": [], "failed": []}

        # Store the original signal receivers
        signals = [post_save, post_delete, pre_save, pre_delete]
        original_receivers = {}

        # Disconnect all signals
        for signal in signals:
            original_receivers[signal] = signal.receivers
            signal.receivers = []

        try:
            # Get all .json files, sort them, and process
            fixture_files = sorted(
                [
                    f.name
                    for f in Path(fixtures_root_path).iterdir()
                    if f.is_file() and f.suffix == ".json"
                ]
            )

            if not fixture_files:
                warning_msg = f"No fixture files found in {fixtures_root_path}"
                logger.warning(warning_msg)
                if verbosity >= 1:
                    self.stdout.write(self.style.WARNING(warning_msg))
                return

            if verbosity >= 1 and continue_on_error:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\nLoading {len(fixture_files)} fixture(s) with --continue-on-error flag:"
                    )
                )

            for fixture_file in fixture_files:
                fixture_file_path = str(Path(fixtures_root_path) / fixture_file)

                try:
                    # Wrap each fixture in its own transaction for isolation
                    with transaction.atomic():
                        # Use call_command instead of subprocess
                        call_command(
                            "loaddata",
                            fixture_file_path,
                            verbosity=0 if verbosity < VERBOSE_LEVEL else 1,
                        )

                    # Success
                    results["success"].append(fixture_file)
                    logger.info("Successfully loaded fixture: %s", fixture_file)
                    if verbosity >= 1:
                        self.stdout.write(
                            self.style.SUCCESS(f"Successfully loaded {fixture_file}"),
                        )

                except Exception as e:
                    # Log the error with full traceback
                    error_msg = f"Failed to load {fixture_file}: {e!s}"
                    logger.exception(error_msg)
                    results["failed"].append((fixture_file, str(e)))

                    if verbosity >= 1:
                        self.stdout.write(self.style.ERROR(error_msg))

                    # Conditional behavior based on flag
                    if continue_on_error:
                        # Continue to next fixture
                        continue
                    # Exit immediately (default behavior)
                    raise

        finally:
            # Restore all signals
            for signal in signals:
                signal.receivers = original_receivers[signal]

        # Summary report (only if continue-on-error mode)
        if continue_on_error and verbosity >= 1:
            self.stdout.write("\n" + "=" * 60)
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Successfully loaded: {len(results['success'])} fixture(s)"
                )
            )
            if results["failed"]:
                self.stdout.write(
                    self.style.ERROR(f"✗ Failed: {len(results['failed'])} fixture(s)")
                )
                for fixture_file, error in results["failed"]:
                    self.stdout.write(f"    - {fixture_file}: {error}")
            self.stdout.write("=" * 60 + "\n")

        # Log final summary
        logger.info(
            f"Fixture loading complete: {len(results['success'])} succeeded, "
            f"{len(results['failed'])} failed"
        )

        # Exit with error code if any failures in continue-on-error mode
        if continue_on_error and results["failed"]:
            raise SystemExit(1)
