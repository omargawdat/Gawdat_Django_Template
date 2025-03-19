from django.core.management.base import BaseCommand

from apps.users.models import User
from apps.users.models.staff import StaffUser
from config.helpers.env import env


class Command(BaseCommand):
    help = "Creates a superuser if one does not exist"

    def handle(self, *args, **options):
        username = env.django_superuser_username
        password = env.django_superuser_password

        if not username or not password:
            self.stdout.write(
                self.style.ERROR("Superuser environment variables are not set"),
            )
            return

        if not User.objects.filter(username=username).exists():
            StaffUser.objects.create_superuser(
                username, password=password.get_secret_value()
            )
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} created successfully"),
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Superuser {username} already exists"),
            )
