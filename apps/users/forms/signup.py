"""Custom signup form for django-allauth headless API."""

import logging

from django import forms

from apps.channel.constants import Language

logger = logging.getLogger(__name__)


class CustomSignupForm(forms.Form):
    """Custom signup form to collect language preference during signup."""

    language = forms.ChoiceField(
        choices=Language.choices,
        required=True,
        initial=Language.ARABIC,
        help_text="Select your preferred language",
    )

    def signup(self, request, user):
        """Save language preference to user instance."""
        logger.info(f"Custom signup form called for user: {user.email}")
        user.language = self.cleaned_data["language"]
        user.save()
        logger.info(f"User language set to: {user.language}")
