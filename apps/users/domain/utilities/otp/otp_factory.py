from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from apps.users.domain.utilities.otp.otp_base_class import OTPSenderBase
from apps.users.domain.utilities.otp.providers.gateway import GatewayOtpService
from apps.users.domain.utilities.phone import PhoneUtils
from apps.users.helpers.constants import SupportedCountry


class OTPFactory:
    @staticmethod
    def get_otp_provider_by_country(phone_number: PhoneNumberField) -> OTPSenderBase:
        country_iso = PhoneUtils.get_country_iso(phone_number)
        if country_iso == SupportedCountry.SAUDI_ARABIA:
            return GatewayOtpService()
        else:
            raise ValidationError("Only Saudi Arabia is supported for OTP services")
