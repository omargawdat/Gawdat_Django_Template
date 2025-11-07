from django.db import transaction

from apps.channel.data_class import DeviceData
from apps.channel.domain.services.device import DeviceService
from apps.users.models.provider import Provider
from apps.users.models.user import User


class ProviderService:
    @staticmethod
    @transaction.atomic
    def complete_provider_profile(
        *,
        user: User,
        company_name: str | None = None,
        language: str | None = None,
        fcm_token: str | None = None,
        device_id: str | None = None,
        device_type: str | None = None,
    ) -> User:
        """Complete provider profile after initial signup."""
        # Update User
        if language:
            user.language = language
            user.save()

        # Create Provider profile
        Provider.objects.create(user=user, company_name=company_name or "")

        # Register device if provided
        if fcm_token and device_type:
            device_data = DeviceData(
                registration_id=fcm_token,
                device_id=device_id,
                type=device_type,
            )
            DeviceService.register_device(user=user, device_data=device_data)

        return user
