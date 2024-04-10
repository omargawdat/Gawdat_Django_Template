import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = "Cleans all migration files in all apps, clears the django_migrations table, and then re-creates and fakes them."

    def handle(self, *args, **kwargs):
        # Step 0: Make migrations and migrate to ensure that the database is up-to-date
        call_command("makemigrations")
        call_command("migrate")
        self.stdout.write(self.style.SUCCESS("Database is up-to-date."))

        # Step 1: Delete all migration records from the django_migrations table
        self.stdout.write(self.style.WARNING("Deleting all records from django_migrations table..."))
        with connections["default"].cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations")
        self.stdout.write(self.style.SUCCESS("All records deleted."))

        # Step 2: Delete all migration files except __init__.py from all apps
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

        # Step 3: Recreate migration files for all apps
        self.stdout.write(self.style.WARNING("Recreating migration files..."))
        call_command("makemigrations")

        # Step 4: Fake apply all migrations
        self.stdout.write(self.style.WARNING("Applying all migrations as fake..."))
        call_command("migrate", "--fake")
        self.stdout.write(self.style.SUCCESS("All migrations have been faked."))
