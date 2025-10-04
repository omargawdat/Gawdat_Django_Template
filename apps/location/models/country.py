import phonenumbers
import pycountry
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


class Country(models.Model):
    code = models.CharField(
        max_length=10,
        unique=True,
        primary_key=True,
        verbose_name=_("Code"),
    )
    flag = models.ImageField(upload_to="flags", verbose_name=_("Flag"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
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

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        # Ensure all MoneyField currencies match the country's currency
        country_currency = self.currency

        # Update currency for all MoneyFields
        if self.app_install_money_inviter_currency != country_currency:
            self.app_install_money_inviter_currency = country_currency
        if self.app_install_money_invitee_currency != country_currency:
            self.app_install_money_invitee_currency = country_currency
        if self.order_money_inviter_currency != country_currency:
            self.order_money_inviter_currency = country_currency
        if self.order_money_invitee_currency != country_currency:
            self.order_money_invitee_currency = country_currency

        super().save(*args, **kwargs)

    @cached_property
    def currency(self) -> str:
        """Get currency code based on country code using Babel"""
        from babel.core import get_global

        # Try to get the currency for this country using Babel
        territory_currencies = get_global("territory_currencies")
        currencies = territory_currencies.get(self.code, [])
        # Return the first currency code (tuple format: (currency_code, start_date, end_date, is_tender))
        currency_data = currencies[0]
        return currency_data[0] if isinstance(currency_data, tuple) else currency_data

    @cached_property
    def phone_code(self) -> str:
        """Get phone code using phonenumbers library"""
        return f"+{phonenumbers.country_code_for_region(self.code)}"

    @cached_property
    def max_phone_length(self) -> int:
        """Get maximum phone number length for this country"""
        example_number = phonenumbers.example_number(self.code)
        national_number = str(example_number.national_number)
        return len(national_number)

    @cached_property
    def name(self) -> str:
        """Get country name from pycountry"""
        country = pycountry.countries.get(alpha_2=self.code)
        return country.name if country else self.code

    @cached_property
    def alpha_3(self) -> str:
        """Get ISO 3166-1 alpha-3 country code"""
        country = pycountry.countries.get(alpha_2=self.code)
        return country.alpha_3 if country else ""

    @cached_property
    def currency_symbol(self) -> str:
        """Get currency symbol"""
        from babel.numbers import get_currency_symbol

        return get_currency_symbol(self.currency, locale="en_US")

    @cached_property
    def phone_example(self) -> str:
        """Get example phone number for this country"""
        example_number = phonenumbers.example_number(self.code)
        return phonenumbers.format_number(
            example_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
