"""Custom account adapter for django-allauth."""

import logging

from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from phonenumber_field.formfields import PhoneNumberField

from apps.users.models.user import User

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
    # PHONE NUMBER STORAGE METHODS
    # ==============================================================================

    def get_phone(self, user):
        """Get phone number and verification status for user."""
        if not user.phone_number:
            return None
        return (str(user.phone_number), user.phone_verified)

    def set_phone(self, user, phone: str, verified: bool):  # noqa: FBT001
        """Set phone number and verification status for user."""
        user.phone_number = phone
        user.phone_verified = verified
        user.save(update_fields=["phone_number", "phone_verified"])
        logger.info(f"Phone set for user_id={user.id}, verified={verified}")

    def set_phone_verified(self, user, phone: str):
        """Mark phone number as verified for user."""
        if str(user.phone_number) == phone:
            user.phone_verified = True
            user.save(update_fields=["phone_verified"])
            logger.info(f"Phone verified for user_id={user.id}")

    def get_user_by_phone(self, phone: str):
        """Lookup user by phone number."""
        try:
            return User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return None

    # ==============================================================================
    # PHONE NUMBER FORM & VALIDATION METHODS
    # ==============================================================================

    def phone_form_field(self, **kwargs):
        """Return form field for phone number input."""
        # Set defaults, allow kwargs to override
        defaults = {
            "required": False,
            "help_text": "Phone number in E164 format (e.g., +966555555555)",
        }
        defaults.update(kwargs)
        return PhoneNumberField(**defaults)

    def clean_phone(self, phone: str) -> str:
        """Validate phone number and ensure it's from supported country."""
        from phonenumbers import parse as parse_phone

        from apps.users.domain.selectors.user import UserSelector

        try:
            phone_obj = parse_phone(phone)
            if not UserSelector.phone_country(phone_obj):
                raise forms.ValidationError(  # noqa: TRY301
                    "Phone number must be from a supported country."
                )
        except Exception as e:
            logger.exception("Phone validation failed")
            raise forms.ValidationError(f"Invalid phone number: {e}") from e
        else:
            return phone

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
                logger.info(f"Verification SMS sent for user_id={user.id}")
        except Exception:
            logger.exception(f"Failed to send verification SMS for user_id={user.id}")
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
            logger.info("Unknown account SMS sent")
        except Exception:
            logger.exception("Failed to send unknown account SMS")
