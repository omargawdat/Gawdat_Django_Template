from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel

from apps.location.constants import LocationNameChoices
from apps.location.models.country import Country
from apps.users.models.customer import Customer


class Address(SoftDeleteModel, models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name=_("Customer"),
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="addresses",
        verbose_name=_("Country"),
    )
    point = gis_models.PointField(srid=4326, verbose_name=_("Location Point"))
    description = models.TextField(verbose_name=_("Description"))
    map_description = models.TextField(
        verbose_name=_("Map Description"),
        help_text=_("Description for the map view"),
        default="",
    )
    location_type = models.CharField(
        max_length=10,
        choices=LocationNameChoices.choices,
        verbose_name=_("Location Type"),
    )
    map_image = models.ImageField(
        upload_to="location/map_images/",
        verbose_name=_("Map Image"),
        help_text=_("Image of the location on the map"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return f"{self.description}"
