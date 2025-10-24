"""Custom signup form for django-allauth headless API."""

import logging

from django import forms
from phonenumber_field.formfields import PhoneNumberField

from apps.channel.constants import Language

logger = logging.getLogger(__name__)


class CustomSignupForm(forms.Form):
    """Custom signup form to collect language and phone during signup."""

    phone = PhoneNumberField(
        required=False,  # Will be validated in clean() for "at least one"
        help_text="Phone number in E164 format (e.g., +966555555555)",
    )

    language = forms.ChoiceField(
        choices=Language.choices,
        required=True,
        initial=Language.ARABIC,
        help_text="Select your preferred language",
    )

    def clean(self):
        """Validate that at least email or phone is provided."""
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")

        # Validate at least one of email or phone is provided
        if not email and not phone:
            raise forms.ValidationError(
                "Please provide either an email address or a phone number."
            )

        # Validate phone if provided
        if phone:
            # Validate phone is from supported country
            from apps.users.domain.selectors.user import UserSelector

            if not UserSelector.phone_country(phone):
                raise forms.ValidationError(
                    "Phone number must be from a supported country."
                )

            # Convert PhoneNumber object to string for allauth compatibility
            cleaned_data["phone"] = str(phone)

        return cleaned_data

    def signup(self, request, user):
        """Save language and phone to user instance."""
        logger.info(f"Custom signup form called for user: {user.email or 'no email'}")

        # Save language preference
        user.language = self.cleaned_data["language"]

        # Save phone if provided
        phone = self.cleaned_data.get("phone")
        if phone:
            user.phone_number = phone
            user.phone_verified = False  # Will be verified through allauth flow
            logger.info(f"Phone number {phone} added to user")

        user.save()
        logger.info(f"User language set to: {user.language}")
