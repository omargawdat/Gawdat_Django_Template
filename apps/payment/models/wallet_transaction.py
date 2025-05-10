from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

from apps.payment.constants import WalletTransactionType
from apps.payment.models.wallet import Wallet
from apps.users.models.admin import AdminUser


class WalletTransaction(models.Model):
    history = HistoricalRecords()
    wallet = models.ForeignKey(
        Wallet, related_name="transactions", on_delete=models.PROTECT
    )
    transaction_type = models.CharField(
        max_length=20, choices=WalletTransactionType.choices
    )
    amount = MoneyField(max_digits=14, decimal_places=2)
    action_by = models.ForeignKey(AdminUser, on_delete=models.PROTECT, null=True)
    transaction_note = models.TextField(max_length=1500, blank=True, default="")
    attachment = models.FileField(
        upload_to="wallet_transactions", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Wallet Transaction")
        verbose_name_plural = _("Wallet Transactions")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Wallet Transaction #{self.pk}"
