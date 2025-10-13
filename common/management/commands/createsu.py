from django.core.management.base import BaseCommand

from apps.users.models import User
from config.helpers.env import env


class Command(BaseCommand):
    help = "Creates a superuser if one does not exist"

    def handle(self, *args, **options):
        email = env.django_superuser_username  # Now expecting email
        password = env.django_superuser_password

        if not email or not password:
            self.stdout.write(
                self.style.ERROR("Superuser environment variables are not set"),
            )
            return

        # Check if user already exists by email or username
        username = email.split("@")[0]

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f"Superuser with email {email} already exists"),
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Superuser with username {username} already exists"
                ),
            )
            return

        # Create superuser
        User.objects.create_superuser(
            email=email, username=username, password=password.get_secret_value()
        )
        self.stdout.write(
            self.style.SUCCESS(f"Superuser {email} created successfully"),
        )
