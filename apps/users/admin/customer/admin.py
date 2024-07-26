from django.contrib import admin
from unfold.contrib.filters.admin import RangeDateFilter

from apps.users.admin.customer.form import CustomerForm
from apps.users.helpers.decorators.customer import CustomerDisplayMixin
from apps.users.models.customer import Customer
from common.base.basemodeladmin import BaseModelAdmin


@admin.register(Customer)
class CustomerAdminBase(BaseModelAdmin, CustomerDisplayMixin):
    #  ---- List View ----
    list_display = ("display_header", "display_phone_number", "date_joined", "name")
    search_fields = ("phone_number",)
    list_filter = (("date_joined", RangeDateFilter),)

    # Change View
    # -----------------------------------------------------------------------------------------
    form = CustomerForm

    def get_fieldsets(self, request, obj=None):
        return (("Personal Information", {"fields": ("phone_number", "image", "date_joined")}),)

    def get_readonly_fields(self, request, obj=None):
        return ("date_joined",)

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
