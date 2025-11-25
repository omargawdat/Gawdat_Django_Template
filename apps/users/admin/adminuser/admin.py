from django.contrib import admin
from django.contrib.auth.hashers import make_password

from apps.users.models.admin import AdminUser
from common.base.admin import BaseModelAdmin

from .change_view import AdminUserChangeView
from .display import AdminUserDisplayMixin
from .list_view import AdminUserListView
from .permissions import AdminUserPermissions


@admin.register(AdminUser)
class AdminUserAdmin(
    AdminUserDisplayMixin,
    AdminUserListView,
    AdminUserChangeView,
    AdminUserPermissions,
    BaseModelAdmin,
):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_superuser=False)

    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
