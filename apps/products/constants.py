from django.db import models
from django.utils.translation import gettext_lazy as _


class BannerTypeChoices(models.TextChoices):
    MAIN_BANNER = "MAIN_BANNER", _("Main Banner")
    SIDE_BANNER = "SIDE_BANNER", _("Side Banner")
