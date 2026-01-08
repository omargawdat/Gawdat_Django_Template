from django.utils.translation import gettext_lazy as _


class BannerGroupChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (_("Information"), {"fields": ("name_ar", "name_en", "order", "is_active")}),
    )
