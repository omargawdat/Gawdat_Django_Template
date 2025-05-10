from django.utils.translation import gettext_lazy as _


class SocialAccountChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            _("Contact Information"),
            {
                "fields": ("email", "phone_number"),
                "description": _("Primary contact details for the organization."),
            },
        ),
        (
            _("Social Media Links"),
            {
                "fields": ("twitter", "instagram", "tiktok"),
                "description": _("Links to social media profiles."),
                "classes": ("collapse",),
            },
        ),
        (
            _("Website"),
            {
                "fields": ("website",),
                "description": _("Official website URL."),
                "classes": ("collapse",),
            },
        ),
    )
