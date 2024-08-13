from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from solo.models import SingletonModel


class SocialAccount(SingletonModel):
    email = models.EmailField(
        validators=[EmailValidator()], verbose_name=_("Email"), blank=True, default=""
    )
    phone_number = PhoneNumberField(
        max_length=15,
        verbose_name=_("Phone Number"),
        help_text=_("Phones start with: '+20'/'+966'"),
        null=True,
        blank=True,
    )
    twitter = models.URLField(blank=True, verbose_name=_("Twitter Account"))
    instagram = models.URLField(blank=True, verbose_name=_("Instagram Account"))
    tiktok = models.URLField(blank=True, verbose_name=_("Tiktok Account"))
    website = models.URLField(blank=True, verbose_name=_("Website"))

    class Meta:
        verbose_name = _("Social Media")
        verbose_name_plural = _("Social Media")

    def __str__(self):
        return "Social Media Configuration"
