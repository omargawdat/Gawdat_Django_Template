from django.core.management.base import BaseCommand

from apps.users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_name = "admin"
        admin_password = "123"
        if not CustomUser.objects.filter(username=admin_name).exists():
            CustomUser.objects.create_superuser(
                username=admin_name,
                password=admin_password,
            )
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
        else:
            self.stdout.write(self.style.WARNING('Super user already exists'))
