"""Custom account adapter for django-allauth."""

import logging

from allauth.account.adapter import DefaultAccountAdapter

logger = logging.getLogger(__name__)


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        # Use default allauth behavior - handles email, username, and password
        user = super().save_user(request, user, form, commit=commit)
        logger.info("Custom account adapter save_user called")
        if commit:
            logger.info(
                f"User created via allauth: user_id={user.id} - Profile completion required"
            )

        return user

    # ==============================================================================
    # OTP CODE GENERATION
    # ==============================================================================
    def generate_phone_verification_code(self) -> str:
        """Generate OTP code for phone verification."""
        import secrets
        import string

        from constance import config

        from config.helpers.env import env

        # In dev/test environments, always use test OTP
        # This allows test phone numbers to login without receiving SMS
        if env.is_testing_sms:
            logger.info("🔧 Using test OTP code (dev/test environment)")
            return config.OTP_TEST_CODE

        # Production: generate secure random code
        # Length controlled by ACCOUNT_PHONE_VERIFICATION_CODE_LENGTH setting (default: 6)
        from django.conf import settings

        code_length = getattr(settings, "ACCOUNT_PHONE_VERIFICATION_CODE_LENGTH", 6)
        code = "".join(secrets.choice(string.digits) for _ in range(code_length))
        return code

    # ==============================================================================
    # SMS SENDING METHODS
    # ==============================================================================

    def send_verification_code_sms(self, user, phone: str, code: str, **kwargs):
        """Send verification code via SMS using existing OTP infrastructure."""
        from phonenumbers import parse as parse_phone

        from config.helpers.env import env

        try:
            phone_obj = parse_phone(phone)

            # Send SMS with the code provided by allauth
            from django.utils.translation import gettext as _

            from apps.channel.domain.utilities.sms import SMSUtils

            message = _("Your verification code is: %(code)s") % {"code": code}
            SMSUtils.send_bulk_message([phone_obj], message)

            # Log the code in test mode for easy testing
            if env.is_testing_sms:
                logger.info(f"📱 PHONE VERIFICATION CODE for {phone}: {code}")
            else:
                logger.info(f"Verification SMS sent to {phone} for user {user.id}")
        except Exception:
            logger.exception(f"Failed to send verification SMS to {phone}")
            raise

    def send_unknown_account_sms(self, phone: str, **kwargs) -> None:
        """Send SMS when verification is requested for unlisted phone."""
        from django.utils.translation import gettext as _
        from phonenumbers import parse as parse_phone

        from apps.channel.domain.utilities.sms import SMSUtils

        try:
            phone_obj = parse_phone(phone)
            message = _(
                "A verification code was requested for this phone number, "
                "but no account exists. Please sign up first."
            )
            SMSUtils.send_bulk_message([phone_obj], message)
            logger.info(f"Unknown account SMS sent to {phone}")
        except Exception:
            logger.exception(f"Failed to send unknown account SMS to {phone}")
