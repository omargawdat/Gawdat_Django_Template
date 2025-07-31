from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from apps.appInfo.models.banner_group import BannerGroup


class Banner(models.Model):
    image = ProcessedImageField(
        upload_to="banners/",
        processors=[ResizeToFit(1200, 800)],
        options={"quality": 90, "optimize": True},
        verbose_name=_("Image Banner"),
    )
    group = models.ForeignKey(
        BannerGroup,
        on_delete=models.CASCADE,
        related_name="banners",
        verbose_name=_("Banner Group"),
    )
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=False)

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")

    def __str__(self):
        return self.group.name
