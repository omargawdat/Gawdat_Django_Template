from django.utils.translation import gettext_lazy as _


class BannerGroupListView:
    list_display = ("display_header", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ("name",)
    search_help_text = _("Search by group name...")
    ordering = ["order"]
