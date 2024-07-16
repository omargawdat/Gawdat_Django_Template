from django.db import models

from apps.users.models import User


class Customer(User):
    name = models.CharField(max_length=100, blank=True, default="")
