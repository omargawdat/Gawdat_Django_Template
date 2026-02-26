from allauth.account import authentication
from allauth.account.adapter import DefaultAccountAdapter
from django.utils.crypto import get_random_string


class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom adapter: skip OTP for social logins, 6-digit numeric codes."""

    def generate_login_code(self) -> str:
        """Generate a 6-digit numeric login code."""
        return get_random_string(length=6, allowed_chars="0123456789")

    def generate_email_verification_code(self) -> str:
        """Generate a 6-digit numeric email verification code."""
        return get_random_string(length=6, allowed_chars="0123456789")

    def is_login_by_code_required(self, login) -> bool:
        """Skip OTP for social and code auth, require for other methods."""
        method = None
        records = authentication.get_authentication_records(self.request)
        if records:
            method = records[-1]["method"]
        if method in ("socialaccount", "code"):
            return False
        return True
