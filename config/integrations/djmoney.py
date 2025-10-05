from apps.location.domain.utils import CountryInfoUtil
from config.settings.base import SUPPORTED_COUNTRY_CODES

# Automatically derive currencies from supported countries
CURRENCIES = tuple(
    CountryInfoUtil.get_currency_code(country_code)
    for country_code in SUPPORTED_COUNTRY_CODES
)
SERIALIZATION_MODULES = {"json": "djmoney.serializers"}
