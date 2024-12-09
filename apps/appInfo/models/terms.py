from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class TermsAndConditions(SingletonModel):
    content_en = models.TextField(
        help_text=_("Terms and Conditions of the website."),
        blank=True,
        verbose_name=_("Content (EN)"),
        default="",
    )
    content_ar = models.TextField(
        help_text=_("Terms and Conditions of the website in Arabic."),
        blank=True,
        verbose_name=_("Content (AR)"),
        default="",
    )

    class Meta:
        verbose_name = _("Terms and Conditions")
        verbose_name_plural = _("Terms and Conditions")

    def __str__(self):
        return "Terms"
