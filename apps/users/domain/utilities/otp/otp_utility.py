import secrets

from django.core.cache import cache
from phonenumber_field.modelfields import PhoneNumberField

from apps.users.models import MobileUser
from apps.users.models import User
from config.settings.base import PASSWORD_RESET_TIMEOUT


class OTPUtility:
    @staticmethod
    def send_otp(phone_number: PhoneNumberField) -> int | None:
        return 0000

        # otp_sender = OTPFactory.get_otp_provider_by_country(phone_number)
        # verification_id = otp_sender.send_otp(phone_number)
        # return verification_id #

    @staticmethod
    def verify_otp(phone_number: PhoneNumberField, otp: str, verification_id: int) -> bool:
        return True
        # otp_sender = OTPFactory.get_otp_provider_by_country(phone_number)
        # return otp_sender.verify_otp(otp, verification_id)

    @staticmethod
    def generate_reset_token(user: User) -> str:
        token = secrets.token_urlsafe(32)
        cache_key = f"password_reset_{token}"
        cache.set(cache_key, user.id, timeout=PASSWORD_RESET_TIMEOUT)
        return token

    @staticmethod
    def get_user_from_reset_token(token: str) -> User | None:
        cache_key = f"password_reset_{token}"
        user_id = cache.get(cache_key)
        if user_id:
            return MobileUser.objects.filter(id=user_id).first()
        return None

    @staticmethod
    def invalidate_reset_token(token: str) -> None:
        cache_key = f"password_reset_{token}"
        cache.delete(cache_key)
