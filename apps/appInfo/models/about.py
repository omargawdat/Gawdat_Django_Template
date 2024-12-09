from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class AboutUs(SingletonModel):
    content_en = models.TextField(
        help_text=_("Information about the company or service."),
        blank=True,
        default="",
    )
    content_ar = models.TextField(
        help_text=_("Information about the company or service in Arabic."),
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = _("About Us")
        verbose_name_plural = _("About Us")

    def __str__(self):
        return "About Us"
