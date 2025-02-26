import os
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save


class Command(BaseCommand):
    help = "Load JSON fixtures from the 'assets/fixtures' directory."

    def handle(self, *args, **kwargs):
        fixtures_root_path = "assets/fixtures"

        if not Path(fixtures_root_path).exists():
            self.stdout.write(
                self.style.ERROR(
                    'The "fixtures" folder does not exist at the project root.',
                ),
            )
            return

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
                [f for f in os.listdir(fixtures_root_path) if f.endswith(".json")],
            )
            for fixture_file in fixture_files:
                fixture_file_path = str(Path(fixtures_root_path) / fixture_file)

                try:
                    # Use call_command instead of subprocess
                    call_command("loaddata", fixture_file_path, verbosity=1)
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully loaded {fixture_file}"),
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to load {fixture_file}: {e!s}"),
                    )
                    raise

        finally:
            # Restore all signals
            for signal in signals:
                signal.receivers = original_receivers[signal]
