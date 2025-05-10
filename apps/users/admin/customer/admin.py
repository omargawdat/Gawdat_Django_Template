from django.contrib import admin

from apps.users.models.customer import Customer
from common.base.admin import BaseModelAdmin

from .change_view import CustomerChangeView
from .display import CustomerDisplayMixin
from .list_view import CustomerListView
from .permissions import CustomerAdminPermissions


@admin.register(Customer)
class CustomerAdmin(
    CustomerDisplayMixin,
    CustomerListView,
    CustomerChangeView,
    CustomerAdminPermissions,
    BaseModelAdmin,
):
    pass
