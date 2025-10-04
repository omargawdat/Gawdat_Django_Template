"""Country Information Utility"""

import phonenumbers
import pycountry
from babel import Locale
from babel.core import get_global
from babel.numbers import get_currency_symbol
from django.utils.translation import get_language


class CountryInfoUtil:
    """Utility class for retrieving country information from various sources"""

    @staticmethod
    def get_currency_code(country_code: str) -> str:
        territory_currencies = get_global("territory_currencies")
        currencies = territory_currencies.get(country_code, [])

        if not currencies:
            raise ValueError(f"No currency found for country code: {country_code}")

        currency_data = currencies[0]
        return currency_data[0] if isinstance(currency_data, tuple) else currency_data

    @staticmethod
    def get_phone_code(country_code: str) -> str:
        code = phonenumbers.country_code_for_region(country_code)
        return f"+{code}"

    @staticmethod
    def get_max_phone_length(country_code: str) -> int:
        example_number = phonenumbers.example_number(country_code)
        national_number = str(example_number.national_number)
        return len(national_number)

    @staticmethod
    def get_phone_example(country_code: str) -> str:
        example_number = phonenumbers.example_number(country_code)
        return phonenumbers.format_number(
            example_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

    @staticmethod
    def get_name(country_code: str, language: str | None = None) -> str:
        lang = language or get_language() or "en"
        locale = Locale.parse(lang)
        return locale.territories.get(country_code, country_code)

    @staticmethod
    def get_alpha_3(country_code: str) -> str:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.alpha_3

    @staticmethod
    def get_currency_symbol(country_code: str, language: str = "en_US") -> str:
        currency_code = CountryInfoUtil.get_currency_code(country_code)
        return get_currency_symbol(currency_code, locale=language)
