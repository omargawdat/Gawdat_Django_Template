from django.db import models
from django.utils.translation import gettext_lazy as _


class SupportedCountry(models.TextChoices):
    SAUDI_ARABIA = "SA", "Saudi Arabia"


class UserType(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    PROVIDER = "provider", "Provider"


class Gender(models.TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
