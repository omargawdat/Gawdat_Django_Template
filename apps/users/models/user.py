from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.channel.constants import Language


class User(AbstractUser):
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    # Override email to make it unique and required
    email = models.EmailField(_("email address"), unique=True)

    language = models.CharField(
        max_length=10, choices=Language.choices, default=Language.ARABIC
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
