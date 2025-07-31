from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit
from simple_history.models import HistoricalRecords

from apps.users.models.customer import Customer


class PopUpBanner(models.Model):
    image = ProcessedImageField(
        upload_to="popups/",
        processors=[ResizeToFit(1200, 800)],
        options={"quality": 90, "optimize": True},
        verbose_name=_("Image Banner"),
    )
    count_per_user = models.PositiveIntegerField(
        verbose_name=_("Display count per user"),
        help_text=_("Number of times this banner will be shown to each user"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this popup banner is active and can be displayed"),
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")

    def __str__(self):
        return f"PopUp #{self.pk}"


class PopUpTracking(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name=_("Customer")
    )
    popup = models.ForeignKey(
        PopUpBanner,
        on_delete=models.CASCADE,
        related_name="views",
        verbose_name=_("Popup Banner"),
    )
    view_count = models.PositiveIntegerField(
        verbose_name=_("View Count"),
        help_text=_("Number of times this user has viewed this banner"),
    )

    class Meta:
        verbose_name = _("Popup Tracking")
        verbose_name_plural = _("Popup Trackings")

    def __str__(self):
        return f"{self.customer} - {self.popup} ({self.view_count} views)"
