from django.contrib.auth.models import BaseUserManager
from polymorphic.managers import PolymorphicManager


class CustomUserManager(PolymorphicManager, BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff as True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser as True.")

        return self.create_user(username, password, **extra_fields)
