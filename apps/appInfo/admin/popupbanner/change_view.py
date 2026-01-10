from django.utils.translation import gettext_lazy as _


class PopUpBannerChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (_("Information"), {"fields": ("image", "count_per_user", "is_active")}),
    )
