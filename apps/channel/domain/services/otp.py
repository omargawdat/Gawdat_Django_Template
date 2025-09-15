import secrets
import string
import time

from constance import config
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from phonenumbers import PhoneNumber

from apps.channel.constants import OTPType
from apps.channel.domain.utilities.sms import SMSUtils
from apps.channel.errors import OTPError
from config.helpers.env import env
from config.settings.base import OTP_EXPIRY_SECONDS
from config.settings.base import OTP_HOURLY_LIMIT
from config.settings.base import OTP_LENGTH
from config.settings.base import OTP_MAX_ATTEMPTS


class OTPUtils:
    @staticmethod
    def _get_cache_key(phone_number: PhoneNumber, otp_type: OTPType) -> str:
        return f"otp:{phone_number}:{otp_type}"

    @staticmethod
    def _get_rate_limit_key(phone_number: PhoneNumber) -> str:
        return f"otp:limit:{phone_number}"

    @staticmethod
    def _should_use_test_otp(phone_number: PhoneNumber) -> bool:
        # Get testing phone numbers from dashboard configuration
        testing_numbers = config.TESTING_PHONE_NUMBERS.strip().split("\n")
        testing_numbers = [num.strip() for num in testing_numbers if num.strip()]

        return (
            str(phone_number) in testing_numbers
            or env.is_development
            or not env.is_sending_sms
        )

    @staticmethod
    def send_otp(
        *,
        phone_number: PhoneNumber,
        otp_auto_complete_token: str | None = None,
        otp_type: OTPType,
    ) -> str:
        rate_key = OTPUtils._get_rate_limit_key(phone_number)
        now = time.time()
        count_data = cache.get(rate_key)

        if count_data is None or now > count_data.get("reset_time", 0):
            count_data = {"count": 0, "reset_time": now + 3600}

        if count_data["count"] >= OTP_HOURLY_LIMIT:
            raise ValidationError(
                OTPError.RATE_LIMIT_EXCEEDED.message,
                code=OTPError.RATE_LIMIT_EXCEEDED.code,
            )

        # Increment the count and update the reset time
        count_data["count"] += 1
        ttl = int(count_data["reset_time"] - now)
        cache.set(rate_key, count_data, timeout=ttl)

        # Generate and store OTP
        should_use_test_otp = OTPUtils._should_use_test_otp(phone_number)
        if should_use_test_otp:
            otp_code = config.OTP_TEST_CODE
        else:
            otp_code = "".join(secrets.choice(string.digits) for _ in range(OTP_LENGTH))

        cache_key = OTPUtils._get_cache_key(phone_number, otp_type)
        cache.set(
            cache_key, {"code": otp_code, "attempts": 0}, timeout=OTP_EXPIRY_SECONDS
        )

        # Only send SMS when not using test OTP
        if not should_use_test_otp:
            message = _("Your verification code for weem is: %(otp_code)s") % {
                "otp_code": otp_code
            }
            if otp_auto_complete_token:
                message += f"\n{otp_auto_complete_token}"
            SMSUtils.send_bulk_message([phone_number], message)
            return _("OTP sent successfully")
        return _("Test OTP in use; SMS not sent")

    @staticmethod
    def validate_correct_otp(
        *, phone_number: PhoneNumber, code: str, otp_type: OTPType
    ) -> bool:
        if env.is_testing_sms and code == "0" * OTP_LENGTH:
            return True

        cache_key = OTPUtils._get_cache_key(phone_number, otp_type)
        otp_data = cache.get(cache_key)

        if not otp_data:
            raise ValidationError(
                OTPError.OTP_NOT_FOUND.message,
                code=OTPError.OTP_NOT_FOUND.code,
            )

        otp_data["attempts"] += 1

        if otp_data["attempts"] >= OTP_MAX_ATTEMPTS:
            cache.delete(cache_key)
            raise ValidationError(
                OTPError.MAX_ATTEMPTS_EXCEEDED.message,
                code=OTPError.MAX_ATTEMPTS_EXCEEDED.code,
            )
        if otp_data["code"] != code:
            cache.set(cache_key, otp_data, timeout=OTP_EXPIRY_SECONDS)
            raise ValidationError(
                OTPError.INVALID_CODE.message,
                code=OTPError.INVALID_CODE.code,
            )

        cache.delete(cache_key)
        return True
