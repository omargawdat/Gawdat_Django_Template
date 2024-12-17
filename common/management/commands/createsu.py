import os

from django.core.management.base import BaseCommand

from apps.users.models import User
from apps.users.models.staff import StaffUser


class Command(BaseCommand):
    help = "Creates a superuser if one does not exist"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.ERROR("Superuser environment variables are not set"),
            )
            return

        if not User.objects.filter(username=username).exists():
            StaffUser.objects.create_superuser(username, password=password)
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} created successfully"),
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Superuser {username} already exists"),
            )
