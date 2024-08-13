from django.contrib import admin
from unfold.contrib.filters.admin import RangeDateFilter

from apps.users.admin.customer.display import CustomerDisplayMixin
from apps.users.admin.customer.form import CustomerForm
from apps.users.models.customer import Customer
from common.base.basemodeladmin import BaseModelAdmin


@admin.register(Customer)
class CustomerAdminBase(BaseModelAdmin, CustomerDisplayMixin):
    #  ---- List View ----
    list_display = (
        "display_header",
        "date_joined",
        "display_is_active",
        "display_is_phone_verified",
    )
    date_hierarchy = "date_joined"
    search_fields = ("phone_number", "full_name")
    search_help_text = "Search by phone number"
    list_filter = (("date_joined", RangeDateFilter),)
    list_filter_submit = True
    ordering = ("-date_joined",)

    # Change View
    # -----------------------------------------------------------------------------------------
    form = CustomerForm

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
                            "email",
                            "birthday",
                            "gender",
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
                            "birthday",
                            "gender",
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

    def has_delete_permission(self, request, customer=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True
