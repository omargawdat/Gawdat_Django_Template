from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicModel

from apps.users.helpers.constants import Gender
from apps.users.helpers.model_manager import CustomUserManager


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
    phone_number = PhoneNumberField(unique=True, help_text="Should start with (+966)")
    is_phone_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to="users/", null=True, blank=True)
    full_name = models.CharField(max_length=255, default="", blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.username = str(self.phone_number)
        super().save(*args, **kwargs)
