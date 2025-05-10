from django.db import models
from django.utils.translation import gettext_lazy as _
from unfold.contrib.forms.widgets import WysiwygWidget


class FAQChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = ((_("FAQ Details"), {"fields": ("order", "question", "answer")}),)
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }
