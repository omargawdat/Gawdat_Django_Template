"""Custom account adapter for django-allauth."""

import logging

from allauth.account.adapter import DefaultAccountAdapter

from apps.channel.data_class import DeviceData
from apps.channel.domain.services.device import DeviceService

logger = logging.getLogger(__name__)


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter that extends django-allauth signup process.

    This adapter:
    1. Saves user language preference during signup
    2. Optionally registers FCM device for push notifications if device data is provided

    Used by django-allauth headless API to customize the save_user flow.
    """

    def save_user(self, request, user, form, commit=True):
        """
        Save user with custom fields from the signup form.

        Args:
            request: The HTTP request object
            user: The user instance being created
            form: The signup form containing additional fields
            commit: Whether to save the user to the database

        Returns:
            The saved user instance
        """
        # Call parent to handle email and password
        user = super().save_user(request, user, form, commit=False)

        # Set user language from form (defaults to Arabic if not provided)
        user.language = form.cleaned_data.get("language", "ar")

        if commit:
            user.save()
            logger.info(f"User created: {user.email} with language: {user.language}")

            # Register FCM device if device fields are provided
            fcm_token = form.cleaned_data.get("fcm_token")
            device_id = form.cleaned_data.get("device_id")
            device_type = form.cleaned_data.get("device_type")

            # Register device if fcm_token and device_type are provided
            if fcm_token and device_type:
                try:
                    device_data = DeviceData(
                        registration_id=fcm_token,
                        device_id=device_id or "",  # Optional, default to empty string
                        type=device_type,
                    )
                    DeviceService.register_device(user=user, device_data=device_data)
                    device_info = (
                        f"Device registered for user {user.email}: {device_type}"
                    )
                    if device_id:
                        device_info = f"{device_info} - {device_id}"
                    logger.info(device_info)
                except Exception:
                    # Log error but don't fail signup if device registration fails
                    logger.exception(f"Failed to register device for user {user.email}")

        return user
