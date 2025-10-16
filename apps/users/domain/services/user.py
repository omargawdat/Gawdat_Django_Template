from apps.channel.domain.services.device import DeviceService
from apps.users.models import User


class UserServices:
    @staticmethod
    def user_logout_all_devices(user: User):
        """Logout user from all devices by deactivating FCM devices."""
        DeviceService.deactivate_all_user_devices(user)

    @staticmethod
    def user_logout_specific_device(
        user: User,
        registration_id: str,
    ):
        """Logout user from specific device by deactivating FCM device."""
        DeviceService.deactivate_user_device(user=user, registration_id=registration_id)
