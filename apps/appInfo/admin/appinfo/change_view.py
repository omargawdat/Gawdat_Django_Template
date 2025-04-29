from django.db import models
from django.utils.translation import gettext_lazy as _
from unfold.contrib.forms.widgets import WysiwygWidget


class AppInfoChangeView:
    filter_horizontal = ()
    # compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            _("Organizational Overview"),
            {
                "fields": (("about_us_ar", "about_us_en"),),
            },
        ),
        (
            _("Terms"),
            {
                "fields": (("terms_ar", "terms_en"),),
            },
        ),
        (
            _("Policy"),
            {
                "fields": (("policy_ar", "policy_en"),),
            },
        ),
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }
