from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None

    def __str__(self):
        return self.email
