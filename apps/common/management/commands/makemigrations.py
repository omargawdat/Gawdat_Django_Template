import os

from django.core.management.commands.makemigrations import Command as MakemigrationsCommand


class Command(MakemigrationsCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)
        os.system("git add -A **/migrations/*.py")
        print("Added new migration files to Git.")
