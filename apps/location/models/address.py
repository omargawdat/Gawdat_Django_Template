from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel

from apps.location.constants import LocationNameChoices
from apps.users.models.customer import Customer


class Address(SoftDeleteModel, models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name=_("Customer"),
    )
    point = gis_models.PointField(srid=4326, verbose_name=_("Location Point"))
    description = models.TextField(verbose_name=_("Description"))
    location_type = models.CharField(
        max_length=10,
        choices=LocationNameChoices.choices,
        verbose_name=_("Location Type"),
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return f"{self.description}"
