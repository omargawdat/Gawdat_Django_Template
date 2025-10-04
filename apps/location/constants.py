from django.db import models
from django.utils.translation import gettext_lazy as _


class LocationNameChoices(models.TextChoices):
    Home = "HOME", _("Home")
    Work = "WORK", _("Work")
