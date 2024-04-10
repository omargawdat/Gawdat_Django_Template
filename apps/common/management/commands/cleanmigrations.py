import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cleans all migration files in all apps and then re-creates them."

    def handle(self, *args, **kwargs):
        apps_folder_path = (
            settings.BASE_DIR / "apps"
        )  # Assuming all apps are within the 'apps' directory at the base level

        self.stdout.write(self.style.WARNING("Cleaning migration files..."))
        for app_name in os.listdir(apps_folder_path):
            app_path = os.path.join(apps_folder_path, app_name)
            migrations_path = os.path.join(app_path, "migrations")

            if os.path.isdir(migrations_path):
                for filename in os.listdir(migrations_path):
                    if filename != "__init__.py" and filename.endswith(".py"):
                        file_path = os.path.join(migrations_path, filename)
                        os.remove(file_path)
                        self.stdout.write(self.style.SUCCESS(f"Removed {file_path}"))

                # Removing compiled Python files in __pycache__
                pycache_path = os.path.join(migrations_path, "__pycache__")
                if os.path.isdir(pycache_path):
                    for filename in os.listdir(pycache_path):
                        if filename.endswith(".pyc"):
                            file_path = os.path.join(pycache_path, filename)
                            os.remove(file_path)
                            self.stdout.write(self.style.SUCCESS(f"Removed {file_path}"))

        self.stdout.write(self.style.WARNING("Recreating migration files..."))
        call_command("makemigrations")
