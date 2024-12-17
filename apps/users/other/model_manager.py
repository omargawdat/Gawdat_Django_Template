from django.contrib.auth.models import BaseUserManager
from polymorphic.managers import PolymorphicManager


class CustomUserManager(PolymorphicManager, BaseUserManager):
    USERNAME_REQUIRED = "The Username field must be set"
    STAFF_REQUIRED = "Superuser must have is_staff as True."
    SUPERUSER_REQUIRED = "Superuser must have is_superuser as True."

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(self.USERNAME_REQUIRED)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(self.STAFF_REQUIRED)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(self.SUPERUSER_REQUIRED)

        return self.create_user(username, password, **extra_fields)
