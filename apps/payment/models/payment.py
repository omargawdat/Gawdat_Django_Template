from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

from apps.payment.constants import PaymentType
from apps.users.models.customer import Customer


class Payment(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Customer"),
    )
    price_before_discount = MoneyField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Price before discount"),
    )
    price_after_discount = MoneyField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Price after discount"),
    )
    payment_type = models.CharField(
        max_length=15,
        choices=PaymentType.choices,
        verbose_name=_("Payment type"),
    )
    is_paid = models.BooleanField(default=False, verbose_name=_("Is paid"))
    payment_charge_id = models.CharField(
        max_length=255,
        default="",
        verbose_name=_("Payment Reference"),
        help_text=_("Reference ID from the payment gateway"),
    )
    bank_transaction_response = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("Bank Transaction Response"),
        help_text=_("Full response from the bank"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["customer", "created_at"]),
        ]

    def __str__(self):
        return f"Payment #{self.id} by {self.customer.username} "
