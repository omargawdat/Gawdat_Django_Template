from django.http import HttpRequest

from apps.users.models.admin import AdminUser


class AdminUserContextLogic:
    def __init__(self, request: HttpRequest, admin_user: AdminUser | None = None):
        self.request = request
        self.admin_user = admin_user

    @property
    def is_superuser(self) -> bool:
        return self.request.user.is_superuser

    @property
    def is_staff(self) -> bool:
        return self.request.user.is_staff

    @property
    def is_creating(self) -> bool:
        return self.admin_user is None

    @property
    def is_created(self) -> bool:
        return self.admin_user is not None
