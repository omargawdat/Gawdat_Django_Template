from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.location.constants import CountryChoices
from apps.location.constants import CurrencyCode


class Country(models.Model):
    code = models.CharField(
        max_length=10,
        unique=True,
        primary_key=True,
        verbose_name=_("Code"),
        choices=CountryChoices.choices,
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        unique=True,
    )
    currency = models.CharField(
        max_length=3, verbose_name=_("Currency"), choices=CurrencyCode.choices
    )
    flag = models.ImageField(upload_to="flags", verbose_name=_("Flag"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    phone_code = models.CharField(max_length=4, verbose_name=_("Number Code"))

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return f"{self.get_code_display()}"
