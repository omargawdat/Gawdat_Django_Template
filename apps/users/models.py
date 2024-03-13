from django.contrib.auth.models import AbstractUser
from django.db.models import CharField


class User(AbstractUser):
    additional_field = CharField(max_length=100)
