from django.utils.translation import gettext_lazy as _


class RegionChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = ((_("Region Information"), {"fields": ("code", "name", "country")}),)
