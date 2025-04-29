from apps.users.api.common.exceptions import InvalidOTPException
from apps.users.models import User


class UserValidator:
    @staticmethod
    def validate_user_is_active(user: User) -> None:
        if not user.is_active:
            raise InvalidOTPException
