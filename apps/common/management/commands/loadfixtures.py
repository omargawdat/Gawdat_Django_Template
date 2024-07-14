import os
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load JSON fixtures from the 'assets/fixtures' directory."

    def handle(self, *args, **kwargs):
        fixtures_root_path = "assets/fixtures"

        if not Path(fixtures_root_path).exists():
            self.stdout.write(
                self.style.ERROR(
                    'The "fixtures" folder does not exist at the project root.'
                )
            )
            return

        # Get all .json files, sort them, and process
        fixture_files = sorted(
            [f for f in os.listdir(fixtures_root_path) if f.endswith(".json")]
        )
        for fixture_file in fixture_files:
            fixture_file_path = Path(fixtures_root_path) / fixture_file
            command = ["python", "manage.py", "loaddata", fixture_file_path]

            try:
                subprocess.run(command, check=True, capture_output=True, text=True)
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully loaded {fixture_file}")
                )
            except subprocess.CalledProcessError as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to load {fixture_file}: {e.stderr}")
                )
