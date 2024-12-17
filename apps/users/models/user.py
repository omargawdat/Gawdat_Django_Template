from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicModel

from apps.users.other.model_manager import CustomUserManager


class User(PolymorphicModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class MobileUser(User):
    phone_number = PhoneNumberField(
        unique=True,
        help_text="Should start with country code as (+966)",
    )
    image = ProcessedImageField(
        upload_to="users/",
        processors=[ResizeToFit(1200, 800)],
        format="JPEG",
        options={"quality": 90, "optimize": True},
        null=True,
    )
    full_name = models.CharField(max_length=255, default="", blank=True)
