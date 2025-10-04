from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


class Country(models.Model):
    code = models.CharField(
        max_length=10,
        unique=True,
        primary_key=True,
        verbose_name=_("Code"),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        unique=True,
    )
    currency = models.CharField(max_length=3, verbose_name=_("Currency"))
    flag = models.ImageField(upload_to="flags", verbose_name=_("Flag"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    phone_code = models.CharField(max_length=4, verbose_name=_("Number Code"))

    app_install_money_inviter = MoneyField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("App Install Money - Inviter"),
        help_text=_("Money awarded to inviter when invitee installs the app."),
    )
    app_install_money_invitee = MoneyField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("App Install Money - Invitee"),
        help_text=_("Money awarded to invitee when they install the app."),
    )
    order_money_inviter = MoneyField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Order Money - Inviter"),
        help_text=_("Money awarded to inviter when invitee places first order."),
    )
    order_money_invitee = MoneyField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Order Money - Invitee"),
        help_text=_("Money awarded to invitee when they place first order."),
    )

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    app_install_money_inviter_currency=models.F("currency")
                ),
                name="app_install_money_inviter_currency_consistency",
                violation_error_message=_(
                    "App install money inviter currency must match country currency."
                ),
            ),
            models.CheckConstraint(
                condition=models.Q(
                    app_install_money_invitee_currency=models.F("currency")
                ),
                name="app_install_money_invitee_currency_consistency",
                violation_error_message=_(
                    "App install money invitee currency must match country currency."
                ),
            ),
            models.CheckConstraint(
                condition=models.Q(order_money_inviter_currency=models.F("currency")),
                name="order_money_inviter_currency_consistency",
                violation_error_message=_(
                    "Order money inviter currency must match country currency."
                ),
            ),
            models.CheckConstraint(
                condition=models.Q(order_money_invitee_currency=models.F("currency")),
                name="order_money_invitee_currency_consistency",
                violation_error_message=_(
                    "Order money invitee currency must match country currency."
                ),
            ),
        ]

    def __str__(self):
        return f"{self.get_code_display()}"

    def save(self, *args, **kwargs):
        # Note: referral_points field doesn't exist in model, commented out to fix
        # if self.currency:
        #     self.referral_points = Money(self.referral_points.amount, self.currency)
        super().save(*args, **kwargs)
