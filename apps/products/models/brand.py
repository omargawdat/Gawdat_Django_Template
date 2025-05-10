from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    logo = ProcessedImageField(
        upload_to="brands/",
        processors=[ResizeToFit(1200, 800)],
        options={"quality": 90, "optimize": True},
        verbose_name=_("Logo"),
    )

    def __str__(self):
        return self.name
