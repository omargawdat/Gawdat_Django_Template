import logging

from django.db.models import QuerySet
from phonenumbers import PhoneNumber

from apps.location.models.country import Country

logger = logging.getLogger(__name__)


class CountrySelector:
    @staticmethod
    def get_active_countries() -> QuerySet:
        return Country.objects.filter(is_active=True)

    @staticmethod
    def country_by_phone(phone_number: PhoneNumber) -> Country:
        return Country.objects.get(pk="UN")  # TODO remove it

        # parsed_number = parse(str(phone_number))
        # country_code = region_code_for_number(parsed_number)
        # country = CountrySelector.country_by_code(country_code)
        # if not country:
        #     if not country:
        #         raise ValidationError(
        #             {"phone_number": _("Country code not found for phone")}
        #         )
        # return country

    @staticmethod
    def country_by_code(code: str) -> Country:
        return CountrySelector.get_active_countries().filter(code=code).first()

    @staticmethod
    def country_by_currency(currency: str) -> Country | None:
        return CountrySelector.get_active_countries().filter(currency=currency).first()
