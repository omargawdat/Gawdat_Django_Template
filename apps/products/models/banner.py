from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from apps.products.constants import BannerTypeChoices


class Banner(models.Model):
    image = ProcessedImageField(
        upload_to="banners/",
        processors=[ResizeToFit(1200, 800)],
        options={"quality": 90, "optimize": True},
        verbose_name=_("Image Banner"),
        null=True,
    )
    banner_type = models.CharField(max_length=255, choices=BannerTypeChoices.choices)

    def __str__(self):
        return self.banner_type
