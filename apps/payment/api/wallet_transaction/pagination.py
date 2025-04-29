from rest_framework.pagination import CursorPagination


class WalletTransactionCursorPagination(CursorPagination):
    page_size = 10
    ordering = "-created_at"
    cursor_query_param = "cursor"
