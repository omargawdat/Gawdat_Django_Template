# from django.contrib import admin
#
# from common.base.basemodeladmin import BaseModelAdmin
#
#
# @admin.register(MyModel)
# class CustomAdminClassBase(BaseModelAdmin, DisplayMixin):
#     #  List View
#     # -----------------------------------------------------------------------------------------
#     list_display = ()
#     list_filter = ()
#     date_hierarchy = None
#     list_per_page = 50
#     list_filter_submit = False
#     list_fullwidth = False
#     list_horizontal_scrollbar_top = False
#     search_fields = ()
#     search_help_text = ""
#     ordering = ()
#
#     def get_ordering(self, request):
#         return ()
#
#     # Change View
#     # -----------------------------------------------------------------------------------------
#     form = None
#     filter_horizontal = ()
#     compressed_fields = False
#     autocomplete_fields = ()
#
#     def get_fieldsets(self, request, obj=None):
#         if obj:
#             return (
#                 ("User Information", {"fields": ()}),
#             )
#         else:
#             return (
#                 ("User Information", {"fields": ()}),
#             )
#
#     def get_readonly_fields(self, request, obj=None):
#         base = ()
#         if obj:
#             return base
#         return base
#
#     def get_inlines(self, request, obj=None):
#         if obj is None:
#             return []
#         return []
#
#     # Permissions
#     # -----------------------------------------------------------------------------------------
#
#     def has_delete_permission(self, request, customer=None):
#         return False
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_change_permission(self, request, obj=None):
#         return False
#
#     # Other
#     # -----------------------------------------------------------------------------------------
