from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from apps.channel.domain.services.device import DeviceService
from apps.users.models import User


class UserServices:
    @staticmethod
    def user_logout_all_devices(user: User):
        tokens = OutstandingToken.objects.filter(user_id=user.id)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        DeviceService.deactivate_all_user_devices(user)

    @staticmethod
    def user_logout_specific_device(
        user: User, refresh_token: str, registration_id: str, device_id: str
    ):
        try:
            token = OutstandingToken.objects.get(token=refresh_token, user_id=user.id)
            BlacklistedToken.objects.get_or_create(token=token)
        except OutstandingToken.DoesNotExist:
            pass  # Token doesn't exist or isn't associated with user

        # Deactivate the specific device
        DeviceService.deactivate_user_device(user=user, registration_id=registration_id)
