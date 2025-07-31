from django.db import models
from django.utils.translation import gettext_lazy as _


class BannerGroup(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Group Name"))
    order = models.PositiveIntegerField(
        verbose_name=_("Order"), help_text=_("Group Ordering Level")
    )
    is_active = models.BooleanField(verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Banner Group")
        verbose_name_plural = _("Banner Group")

    def __str__(self):
        return self.name
