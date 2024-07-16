from django.contrib import admin

from common.base.modeladmin import ModelAdmin


class MyModel:
    pass


@admin.register(MyModel)
class CustomAdminClass(ModelAdmin):
    #  List View
    # -----------------------------------------------------------------------------------------
    list_display = ()
    search_fields = ()
    list_filter = ()
    date_hierarchy = None
    actions_list = []
    actions_row = []

    list_per_page = 50
    list_filter_submit = False
    list_fullwidth = False
    show_facets = admin.ShowFacets.ALWAYS
    list_horizontal_scrollbar_top = False

    def get_ordering(self, request):
        return ()

    # Change View
    # -----------------------------------------------------------------------------------------
    filter_horizontal = ()
    readonly_preprocess_fields = {}
    formfield_overrides = {}
    actions_detail = []
    actions_submit_line = []
    compressed_fields = False
    autocomplete_fields = ()

    def get_fieldsets(self, request, obj=None):
        return (
            ("Name", {"fields": ("field_one, field_two")}),
            ("Name", {"fields": ("field_one, field_two")}),
        )

    def get_readonly_fields(self, request, obj=None):
        return ()

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        return []

    # Permissions
    # -----------------------------------------------------------------------------------------

    def has_delete_permission(self, request, customer=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
