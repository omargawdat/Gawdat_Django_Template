from django.utils.translation import gettext_lazy as _


class OnboardingListView:
    list_display = ("display_header", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = False
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = (
        "title",
        "text",
        "sub_text",
    )
    search_help_text = _("Search by title, text, or sub_text")
    ordering = ("order",)
