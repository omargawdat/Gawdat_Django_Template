import secrets
import string
from datetime import datetime

from django.core.cache import cache
from django.utils import timezone


class OTPUtility:
    MAX_ATTEMPTS = 3
    PREFIX = "otp_"

    @staticmethod
    def generate_otp(length: str = 5) -> str:
        otp = "".join(secrets.choice(string.digits) for _ in range(length))
        return otp

    @staticmethod
    def _remaining_seconds(expires_at_iso: str) -> int:
        dt = datetime.fromisoformat(expires_at_iso)
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        return max(0, int((dt - timezone.now()).total_seconds()))

    @classmethod
    def verify_or_bust(cls, email: str, otp_input: str) -> None:
        cache_key = f"{cls.PREFIX}{email}"
        record = cache.get(cache_key)
        if not record:
            raise ValueError("OTP has expired or is invalid.")

        # TTL
        try:
            remaining = cls._remaining_seconds(record["expires_at"])
        except Exception as err:
            cache.delete(cache_key)
            raise ValueError("OTP has expired. Please request a new one.") from err
        if remaining <= 0:
            cache.delete(cache_key)
            raise ValueError(" OTP has expired. Please request a new one.")

        # Attempts
        attempts = int(record.get("attempts", 0))
        if attempts >= cls.MAX_ATTEMPTS:
            cache.delete(cache_key)
            raise ValueError("Too many attempts. Please request a new OTP.")

        # Match
        expected = str(record.get("otp", "")).strip()
        got = str(otp_input).strip()
        if got != expected:
            attempts += 1
            cache.set(cache_key, {**record, "attempts": attempts}, timeout=remaining)
            left = max(0, cls.MAX_ATTEMPTS - attempts)
            raise ValueError(f"Invalid OTP. {left} attempt(s) remaining.")

        # success: consume
        cache.delete(cache_key)
