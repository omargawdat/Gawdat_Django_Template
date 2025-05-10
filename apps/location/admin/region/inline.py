from django_model_suite.admin import BaseTabularInline

from apps.location.models.region import Region

from .permissions import RegionInlinePermissions


class RegionInline(RegionInlinePermissions, BaseTabularInline):
    model = Region
    extra = 0
    show_change_link = True
    fields = ()
    autocomplete_fields = ()
