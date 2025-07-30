from django.utils.translation import gettext_lazy as _


class ContactUsListView:
    list_display = (
        "display_header",
        "display_contact_type",
        "display_created_at",
        "has_checked",
    )
    list_editable = ("has_checked",)
    list_filter = ("contact_type",)
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ("customer__phone_number",)
    search_help_text = _("Search by customer phone...")

    def get_ordering(self, request):
        return ()
