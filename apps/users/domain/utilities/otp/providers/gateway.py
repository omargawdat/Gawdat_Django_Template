import requests
from django.core.exceptions import ValidationError
from phonenumbers import PhoneNumber

from apps.users.domain.utilities.otp.otp_base_class import OTPSenderBase
from config.settings.base import env

HTTP_OK = 200
REQUEST_TIMEOUT = 10


class GatewayOtpService(OTPSenderBase):
    @staticmethod
    def send_otp(phone_number: PhoneNumber) -> int | None:
        api_id = env("API_ID")
        api_password = env("API_PASSWORD")
        brand = env("BRAND")
        sender_id = env("SENDER_ID")
        sanitized_phone_number = str(phone_number).lstrip("+")
        url = f"http://REST.GATEWAY.SA/api/Verify?api_id={api_id}&api_password={api_password}&brand={brand}&phonenumber={sanitized_phone_number}&sender_id={sender_id}"

        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code != HTTP_OK or response.json().get("status") != "S":
            error_message = response.json().get("message", "Failed to send OTP")
            raise ValidationError(error_message)

        verification_id = response.json().get("verfication_id")
        if verification_id:
            return int(verification_id)
        return None

    @staticmethod
    def verify_otp(otp: str, verification_id: int) -> bool:
        url = f"http://REST.GATEWAY.SA/api/VerifyStatus?verfication_id={verification_id}&verfication_code={otp}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)

        return response.json().get("status") == "S"
