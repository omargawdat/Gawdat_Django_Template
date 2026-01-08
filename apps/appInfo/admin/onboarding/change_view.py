from django.utils.translation import gettext_lazy as _


class OnboardingChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            _("Main Information"),
            {"fields": ("title", "order", "is_active")},
        ),
        (
            _("Content"),
            {"fields": ("text", "sub_text")},
        ),
        (
            _("Media"),
            {"fields": ("image",)},
        ),
    )
