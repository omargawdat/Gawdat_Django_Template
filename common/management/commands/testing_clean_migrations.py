from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Deletes all migration files in all apps."

    def handle(self, *args, **kwargs):
        apps_folder_path = Path(settings.BASE_DIR) / "apps"
        self.stdout.write(self.style.WARNING("Cleaning migration files..."))
        for app_path in apps_folder_path.iterdir():
            if app_path.is_dir():
                migrations_path = app_path / "migrations"
                if migrations_path.is_dir():
                    for file_path in migrations_path.iterdir():
                        if (
                            file_path.name != "__init__.py"
                            and file_path.suffix == ".py"
                        ):
                            file_path.unlink()
                            self.stdout.write(
                                self.style.SUCCESS(f"Removed {file_path}"),
                            )
        self.stdout.write(self.style.SUCCESS("All migration files have been cleaned."))
