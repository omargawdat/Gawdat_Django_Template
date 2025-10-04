from typing import TYPE_CHECKING

from phonenumbers import PhoneNumber

from apps.channel.domain.utilities.sms_helpers.base.base_class import OTPSenderBase
from apps.channel.domain.utilities.sms_helpers.providers.oursms import OurSMSUtils
from apps.channel.domain.utilities.sms_helpers.providers.smsmisr import SMSMisrUtils
from apps.location.domain.selector.country import CountrySelector

if TYPE_CHECKING:
    from apps.location.models.country import Country


class SMSProviderFactory:
    @staticmethod
    def get_sms_provider_by_country(phone: PhoneNumber) -> OTPSenderBase:
        country: Country = CountrySelector.country_by_phone(phone)

        if country.code == "SA":
            return OurSMSUtils()
        elif country.code == "EG":
            return SMSMisrUtils()
        else:
            raise NotImplementedError("Country not supported")
