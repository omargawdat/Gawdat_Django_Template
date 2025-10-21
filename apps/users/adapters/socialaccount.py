"""Custom social account adapter for django-allauth."""

import logging

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from apps.channel.constants import Language

logger = logging.getLogger(__name__)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter for social authentication flows."""

    def pre_social_login(self, request, sociallogin):
        """Called before social login is processed."""
        logger.info(
            f"Pre-social login called - Provider: {sociallogin.account.provider}, "
            f"Email: {sociallogin.user.email}, Is existing: {sociallogin.is_existing}"
        )

    def populate_user(self, request, sociallogin, data):
        """Populate user fields from social account data."""
        user = super().populate_user(request, sociallogin, data)

        # Set default language (can be overridden by signup form)
        if not user.language:
            user.language = Language.ARABIC
            logger.info(f"Setting default language to {user.language} for {user.email}")

        logger.info(
            f"Populate user called - Provider: {sociallogin.account.provider}, "
            f"Email: {user.email}, Language: {user.language}"
        )

        return user

    def save_user(self, request, sociallogin, form=None):
        """Save user instance during social signup."""
        user = super().save_user(request, sociallogin, form)

        logger.info(
            f"Social account save_user called - Provider: {sociallogin.account.provider}, "
            f"Email: {user.email}, Language: {user.language}, Form: {form}"
        )

        return user
