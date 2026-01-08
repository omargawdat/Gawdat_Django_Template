from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import RangeDateFilter


class NotificationListView:
    list_display = (
        "display_header",
        "display_notification_type",
        "title",
        "display_message",
        "display_created_time",
        "display_is_read",
    )
    list_editable = ()
    list_filter = (
        ("created_at", RangeDateFilter),
        "notification_type",
    )
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = True
    list_fullwidth = True
    list_horizontal_scrollbar_top = True
    search_fields = ["id", "title", "message_body"]
    search_help_text = _("Search By Notification ID, title, body...🔍")
    ordering = ["-created_at"]
