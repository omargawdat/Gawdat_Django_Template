from apps.users.api.exceptions import InactiveUserError
from apps.users.models import User


class UserValidator:
    @staticmethod
    def validate_user_is_active(user: User) -> None:
        if not user.is_active:
            raise InactiveUserError
