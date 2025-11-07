from apps.users.models.provider import Provider
from common.base.admin import BaseTabularInline

from .permissions import ProviderInlinePermissions


class ProviderInline(ProviderInlinePermissions, BaseTabularInline):
    model = Provider
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
