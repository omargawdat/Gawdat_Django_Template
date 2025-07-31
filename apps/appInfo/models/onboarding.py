from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit


class Onboarding(models.Model):
    title = models.CharField(max_length=255, default="")
    image = ProcessedImageField(
        upload_to="onboarding/",
        processors=[ResizeToFit(1200, 800)],
        options={"quality": 90, "optimize": True},
        verbose_name=_("Image"),
    )
    text = models.TextField(
        verbose_name=_("Text"),
        max_length=75,
        help_text=_("You can only wirte 75 characters."),
    )
    sub_text = models.TextField(
        verbose_name=_("Sub Text"),
        default="",
        max_length=50,
        help_text=_("You can only wirte 50 characters."),
    )
    order = models.PositiveIntegerField(verbose_name=_("Order"))
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=False)

    class Meta:
        verbose_name = _("Onboarding")
        verbose_name_plural = _("Onboarding")
        ordering = ["order"]

    def __str__(self):
        return str(self.order)
