from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

from apps.channel.constants import Language
from apps.users.model_manager import CustomUserManager


class User(PolymorphicModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(_("Email"), default="", blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    language = models.CharField(
        max_length=10, choices=Language.choices, default=Language.ARABIC
    )

    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.password:
            try:
                identify_hasher(self.password)
            except ValueError:
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
