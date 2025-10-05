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
    REFERRAL = "REFERRAL", _("Referral")
    REFERRAL_APP_INSTALL_INVITER = (
        "REFERRAL_APP_INSTALL_INVITER",
        _("Referral - App Install (Inviter)"),
    )
    REFERRAL_APP_INSTALL_INVITEE = (
        "REFERRAL_APP_INSTALL_INVITEE",
        _("Referral - App Install (Invitee)"),
    )
    REFERRAL_ORDER_INVITER = (
        "REFERRAL_ORDER_INVITER",
        _("Referral - First Order (Inviter)"),
    )
    REFERRAL_ORDER_INVITEE = (
        "REFERRAL_ORDER_INVITEE",
        _("Referral - First Order (Invitee)"),
    )


class ReferralType(models.TextChoices):
    APP_INSTALL = "APP_INSTALL", _("App Install")
    FIRST_ORDER = "FIRST_ORDER", _("First Order")


class PaymentType(models.TextChoices):
    other = "other", _("Other")
