from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from apps.location.models.country import Country


class Region(models.Model):
    code = models.CharField(
        max_length=10, unique=True, primary_key=True, verbose_name=_("Code")
    )
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, verbose_name=_("Country")
    )
    geometry = models.GeometryField(srid=4326, verbose_name=_("Geometry"))

    def __str__(self):
        return f"{self.country.code}_{self.code}"

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
