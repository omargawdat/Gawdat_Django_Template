import subprocess

from django.core.management.commands.makemigrations import (
    Command as MakemigrationsCommand,
)


class Command(MakemigrationsCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)
        subprocess.Popen(["/usr/bin/git", "add", "-A", "**/migrations/*.py"])  # noqa: S603
