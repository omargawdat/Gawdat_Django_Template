from rest_framework.pagination import CursorPagination


class NotificationCursorPagination(CursorPagination):
    page_size = 10
    ordering = ("-created_at", "-id")
    cursor_query_param = "cursor"
    page_size_query_param = "page_size"
