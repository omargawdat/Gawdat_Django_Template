from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class AppInfo(SingletonModel):
    about_us = models.TextField(
        verbose_name=_("About Us"),
        help_text=_("Description about the organization."),
        blank=True,
    )
    terms = models.TextField(
        verbose_name=_("Terms of Service"),
        help_text=_("Terms and conditions for organization."),
        blank=True,
    )
    policy = models.TextField(
        verbose_name=_("Privacy Policy"),
        help_text=_("Privacy policy details for the organization."),
        blank=True,
    )

    class Meta:
        verbose_name = _("Application Information")
        verbose_name_plural = _("Application Information")

    def __str__(self):
        return str(_("App Information"))
