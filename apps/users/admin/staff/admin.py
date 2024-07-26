from django.contrib import admin

from apps.users.admin.staff.form import StaffForm
from apps.users.helpers.decorators.staff import StaffDisplay
from apps.users.helpers.hash_password import HashPasswordMixin
from apps.users.models.staff import StaffUser
from common.base.basemodeladmin import BaseModelAdmin


@admin.register(StaffUser)
class StaffUserAdmin(HashPasswordMixin, BaseModelAdmin, StaffDisplay):
    # List View
    # -----------------------------------------------------------------------------------------
    list_display = ("display_header", "is_active", "is_superuser", "date_joined")
    search_fields = ["username"]
    list_filter = ("is_active", "is_superuser", "groups")
    ordering = ("username",)

    # Change View
    # -----------------------------------------------------------------------------------------
    form = StaffForm
    filter_horizontal = ("groups", "user_permissions")

    def get_fieldsets(self, request, obj=None):
        common_fields = ("username", "password", "phone_number", "image")
        if obj:
            return (
                ("Information", {"fields": (*common_fields, "date_joined")}),
                (
                    "Permissions",
                    {"fields": ("is_active", "is_superuser", "groups", "user_permissions")},
                ),
            )
        return (("Information", {"fields": (*common_fields, "groups", "user_permissions")}),)

    def get_readonly_fields(self, request, obj=None):
        base = ("date_joined", "is_superuser")
        if obj:
            return base
        return base

    # Permissions
    # -----------------------------------------------------------------------------------------
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    # Other
    # -----------------------------------------------------------------------------------------
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_superuser=False)

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super().save_model(request, obj, form, change)
