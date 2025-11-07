import logging

from django.contrib.auth.base_user import AbstractBaseUser

from apps.channel.constants import Language
from apps.users.constants import UserType
from apps.users.models import User

logger = logging.getLogger(__name__)


class UserSelector:
    @staticmethod
    def group_users_by_type(
        users: list[AbstractBaseUser],
    ) -> dict[UserType, list[User]]:
        """Group users by their type."""
        user_groups = {}
        for user in users:
            if hasattr(user, "customer"):
                user_type = UserType.CUSTOMER
            else:
                logger.exception("Unsupported user type: %s", type(user))
                continue

            if user_type not in user_groups:
                user_groups[user_type] = []
            user_groups[user_type].append(user)

        return user_groups

    @staticmethod
    def group_by_language(users) -> dict[Language, list[User]]:
        """Group users by their preferred language."""
        user_groups = {}
        for user in users:
            language = user.language
            if language not in user_groups:
                user_groups[language] = []
            user_groups[language].append(user)

        return user_groups
