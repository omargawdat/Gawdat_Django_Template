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

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or self.username or f"User {self.id}"

    @property
    def is_profile_complete(self) -> bool:
        """Check if user has completed profile setup by checking for related profiles."""
        return hasattr(self, "customer") or hasattr(self, "adminuser")
