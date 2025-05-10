from apps.location.models.country import Country
from common.base.admin import BaseTabularInline

from .permissions import CountryInlinePermissions


class CountryInline(CountryInlinePermissions, BaseTabularInline):
    model = Country
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
