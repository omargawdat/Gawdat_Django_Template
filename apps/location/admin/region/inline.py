from apps.location.models.region import Region
from common.base.admin import BaseTabularInline

from .permissions import RegionInlinePermissions


class RegionInline(RegionInlinePermissions, BaseTabularInline):
    model = Region
    extra = 0
    show_change_link = True
    fields = ()
    autocomplete_fields = ()
