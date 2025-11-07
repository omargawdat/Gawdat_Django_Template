from apps.users.models.customer import Customer
from common.base.admin import BaseTabularInline

from .permissions import CustomerInlinePermissions


class CustomerInline(CustomerInlinePermissions, BaseTabularInline):
    model = Customer
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
