import secrets
import string
import time

from django.core.cache import cache
from django.core.exceptions import ValidationError
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
    def send_otp(*, phone_number: PhoneNumber, otp_type: OTPType):
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
        otp_code = "".join(secrets.choice(string.digits) for _ in range(OTP_LENGTH))
        cache_key = OTPUtils._get_cache_key(phone_number, otp_type)
        cache.set(
            cache_key, {"code": otp_code, "attempts": 0}, timeout=OTP_EXPIRY_SECONDS
        )

        message = f"Your verification code is: {otp_code}. Valid for {OTP_EXPIRY_SECONDS // 60} minutes."
        SMSUtils.send_bulk_message([phone_number], message)

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
