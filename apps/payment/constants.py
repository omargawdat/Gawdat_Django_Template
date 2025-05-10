from django.db import models
from django.utils.translation import gettext_lazy as _


class WalletTransactionType(models.TextChoices):
    REFUND = "REFUND", _("Refund")
    FINE = "FINE", _("Fine")
    PAYOUT = "PAYOUT", _("Payout")
    CHARGING = "CHARGING", _("Charging")
    ORDER_PAYMENT = "ORDER_PAYMENT", _("Order Payment")
    CANCEL_ORDER = "CANCEL_ORDER", _("Cancel Order")
    SHARE = "SHARE", _("Share")
    CASH_RECEIVE = "CASH_RECEIVE", _("Cash Receive")
