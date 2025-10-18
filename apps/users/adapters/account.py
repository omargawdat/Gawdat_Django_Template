"""Custom account adapter for django-allauth."""

import logging

from allauth.account.adapter import DefaultAccountAdapter

logger = logging.getLogger(__name__)


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        # Use default allauth behavior - handles email, username, and password
        user = super().save_user(request, user, form, commit=commit)

        if commit:
            logger.info(
                f"User created via allauth: {user.email} - Profile completion required"
            )

        return user
