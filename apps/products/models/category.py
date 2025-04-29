from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = ProcessedImageField(
        upload_to="categories/",
        processors=[ResizeToFit(1200, 800)],
        options={"quality": 90, "optimize": True},
        verbose_name=_("Image"),
    )

    def __str__(self) -> str:
        return self.name
