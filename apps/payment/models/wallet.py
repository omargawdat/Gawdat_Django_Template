from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

from apps.users.models import User


class Wallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wallet",
        verbose_name=_("User"),
    )
    balance = MoneyField(max_digits=14, decimal_places=2, verbose_name=_("Balance"))
    is_use_wallet_in_payment = models.BooleanField(
        default=True, verbose_name=_("Use Wallet in Payment")
    )
    last_update = models.DateTimeField(auto_now=True, verbose_name=_("Last Update"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")

    def __str__(self):
        return f"{self.user}'s Wallet"
