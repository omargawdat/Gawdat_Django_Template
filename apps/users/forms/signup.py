"""Custom signup form for django-allauth headless API."""

from django import forms

from apps.channel.constants import Language


class CustomSignupForm(forms.Form):
    """
    Custom signup form that collects additional user information.

    This form extends the default allauth signup to collect:
    - User language preference (optional, defaults to Arabic)
    - Optional FCM device registration details for push notifications

    Device fields (all optional):
    - fcm_token: Firebase Cloud Messaging token (required if registering device)
    - device_type: Platform type - android, ios, or web (required if fcm_token provided)
    - device_id: Unique device identifier (optional)

    The form integrates seamlessly with django-allauth headless API
    and appears automatically in the OpenAPI specification.
    """

    language = forms.ChoiceField(
        choices=Language.choices,
        required=False,
        initial=Language.ARABIC,
        help_text="User's preferred language for the application",
    )

    # Optional device fields for FCM push notifications
    fcm_token = forms.CharField(
        required=False,
        max_length=255,
        help_text="Firebase Cloud Messaging registration token for push notifications",
    )

    device_id = forms.CharField(
        required=False,
        max_length=255,
        help_text="Unique device identifier (optional)",
    )

    device_type = forms.ChoiceField(
        choices=[
            ("android", "Android"),
            ("ios", "iOS"),
            ("web", "Web"),
        ],
        required=False,
        help_text="Device platform type (required if fcm_token is provided)",
    )

    def clean(self):
        """
        Validate device field dependencies.

        Rules:
        - All device fields are optional
        - If fcm_token is provided, device_type must also be provided
        - device_id is always optional
        """
        cleaned_data = super().clean()
        fcm_token = cleaned_data.get("fcm_token")
        device_type = cleaned_data.get("device_type")

        # If fcm_token provided, device_type is required
        if fcm_token and not device_type:
            raise forms.ValidationError(
                {"device_type": "device_type is required when fcm_token is provided."}
            )

        return cleaned_data

    def signup(self, request, user):
        """
        Required method for allauth custom signup forms.

        This method is called after the user is saved by the adapter.
        We don't need to do anything here as all our logic is handled
        in the CustomAccountAdapter.save_user() method.
        """
