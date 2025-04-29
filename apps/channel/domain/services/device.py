from django.contrib.auth import get_user_model
from fcm_django.admin import FCMDevice

from apps.channel.data_class import DeviceData

User = get_user_model()


class DeviceService:
    @staticmethod
    def register_device(
        *,
        user: User,
        device_data: DeviceData,
    ) -> None:
        FCMDevice.objects.update_or_create(
            registration_id=device_data.registration_id,
            device_id=device_data.device_id,
            defaults={
                "user": user,
                "type": device_data.type,
                "active": True,
            },
        )

    @staticmethod
    def deactivate_user_device(
        *, user: User, registration_id: str, device_id: str
    ) -> None:
        FCMDevice.objects.filter(
            user=user, registration_id=registration_id, device_id=device_id
        ).update(active=False)

    @staticmethod
    def deactivate_all_user_devices(user: User) -> None:
        FCMDevice.objects.filter(user=user).update(active=False)

    @staticmethod
    def get_active_devices_for_users(users: list[User]) -> list[FCMDevice]:
        """Get all active FCM devices for the given users"""
        return FCMDevice.objects.filter(user__in=users, active=True)
