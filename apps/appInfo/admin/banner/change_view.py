from django.utils.translation import gettext_lazy as _


class BannerChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ("group",)
    fieldsets = (
        (
            _("Banner"),
            {"fields": ("image", "group", "is_active")},
        ),
    )
