from apps.location.models.address import Address
from common.base.admin import BaseTabularInline

from .permissions import AddressInlinePermissions


class AddressInline(AddressInlinePermissions, BaseTabularInline):
    model = Address
    extra = 0
    show_change_link = True
    tab = True
    fields = ("description", "location_type")
    autocomplete_fields = ()
