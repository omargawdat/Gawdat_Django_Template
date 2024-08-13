from django.contrib import admin
from unfold.contrib.filters.admin import RangeDateFilter

from apps.users.admin.provider.display import ProviderDisplayMixin
from apps.users.admin.provider.form import ProviderForm
from apps.users.helpers.hash_password import HashPasswordMixin
from apps.users.models.provider import Provider
from common.base.basemodeladmin import BaseModelAdmin


@admin.register(Provider)
class ProviderAdmin(HashPasswordMixin, BaseModelAdmin, ProviderDisplayMixin):
    #  List View
    # -----------------------------------------------------------------------------------------
    list_display = (
        "display_header",
        "date_joined",
        "display_is_active",
        "display_is_phone_verified",
    )
    list_filter = ("is_active", "is_staff", ("date_joined", RangeDateFilter))
    list_filter_submit = True

    date_hierarchy = "date_joined"
    search_fields = ("phone_number", "full_name")
    search_help_text = "Search by phone number"
    ordering = ("-date_joined",)

    # Change View
    # -----------------------------------------------------------------------------------------
    form = ProviderForm
    compressed_fields = True

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (
                    "User Information",
                    {
                        "fields": (
                            "phone_number",
                            "password",
                            "full_name",
                            "image",
                            "gender",
                            "birthday",
                            "email",
                        )
                    },
                ),
                ("Active", {"fields": ("is_active", "is_phone_verified", "date_joined")}),
            )
        else:
            return (
                (
                    "User Information",
                    {
                        "fields": (
                            "is_phone_verified",
                            "phone_number",
                            "password",
                            "email",
                            "full_name",
                            "image",
                            "gender",
                            "birthday",
                        )
                    },
                ),
            )

    def get_readonly_fields(self, request, obj=None):
        base = ("date_joined",)
        if obj:
            return base
        return base

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        return []

    # Permissions
    # -----------------------------------------------------------------------------------------

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    # Other
    # -----------------------------------------------------------------------------------------
