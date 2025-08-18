from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class SystemConfig(SingletonModel):
    cancellation_fees = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Cancellation Fees"),
        help_text=_("cancellation feed."),
    )
    referral_points = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Referral Points"),
        help_text=_("Points awarded for referring a new user."),
    )

    class Meta:
        verbose_name = _("System Configuration")
        verbose_name_plural = _("System Configuration")

    def __str__(self):
        return str(_("System Configuration"))
