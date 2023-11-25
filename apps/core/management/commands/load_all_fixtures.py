import os
import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load all fixtures for all apps in the apps directory.'

    def handle(self, *args, **kwargs):
        # Step 1: Open the apps folder
        apps_folder_path = 'apps'

        # Check if apps folder exists
        if not os.path.exists(apps_folder_path):
            self.stdout.write(self.style.ERROR('The "apps" folder does not exist.'))
            return

        for app_name in os.listdir(apps_folder_path):
            fixture_folder_path = os.path.join(apps_folder_path, app_name, 'fixtures')

            # Check if the fixtures folder exists in the app directory
            if os.path.exists(fixture_folder_path):
                for fixture_file in os.listdir(fixture_folder_path):
                    if fixture_file.endswith('.json'):
                        fixture_file_path = os.path.join(fixture_folder_path, fixture_file)
                        command = f"python manage.py loaddata {fixture_file_path}"

                        try:
                            subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {fixture_file}'))
                        except subprocess.CalledProcessError as e:
                            self.stdout.write(self.style.ERROR(f'Failed to load {fixture_file}: {e.stderr}'))
