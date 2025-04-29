from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderChoices(models.TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    NOT_SELECTED = "NS", _("Not Selected")


class UserType(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    PROVIDER = "provider", "Provider"
