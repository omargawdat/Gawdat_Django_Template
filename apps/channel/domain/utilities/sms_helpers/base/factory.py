from typing import TYPE_CHECKING

from phonenumbers import PhoneNumber

from apps.channel.domain.utilities.sms_helpers.base.base_class import OTPSenderBase
from apps.channel.domain.utilities.sms_helpers.providers.oursms import OurSMSUtils
from apps.channel.domain.utilities.sms_helpers.providers.smsmisr import SMSMisrUtils
from apps.location.domain.selector.country import CountrySelector

if TYPE_CHECKING:
    from apps.location.models.country import Country


class SMSProviderFactory:
    """
    Factory for getting SMS providers based on country code.

    To add a new provider:
    1. Import the provider class
    2. Add an entry to PROVIDER_REGISTRY mapping country code to provider class
    """

    # Registry mapping country codes to SMS provider classes
    PROVIDER_REGISTRY: dict[str, type[OTPSenderBase]] = {
        "SA": OurSMSUtils,
        "EG": SMSMisrUtils,
    }

    # Default provider for countries not in registry
    DEFAULT_PROVIDER: type[OTPSenderBase] = OurSMSUtils

    @classmethod
    def get_sms_provider_by_country(cls, phone: PhoneNumber) -> OTPSenderBase:
        country: Country = CountrySelector.country_by_phone(phone)

        provider_class = cls.PROVIDER_REGISTRY.get(country.code, cls.DEFAULT_PROVIDER)
        return provider_class()
