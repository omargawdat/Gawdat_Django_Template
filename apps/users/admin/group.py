from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import ModelForm

from common.base.basemodeladmin import BaseModelAdmin

admin.site.unregister(Group)


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"


@admin.register(Group)
class GroupAdminBase(BaseModelAdmin):
    #  List View
    # -----------------------------------------------------------------------------------------
    search_fields = ("name",)
    ordering = ("name",)

    # Change View
    # -----------------------------------------------------------------------------------------
    form = GroupForm
    filter_horizontal = ("permissions",)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if fieldsets is None:
            fieldsets = (
                (
                    None,
                    {
                        "fields": ("name", "permissions"),
                    },
                ),
            )
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if readonly_fields is None:
            readonly_fields = []
        return readonly_fields

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "permissions":
            qs = kwargs.get("queryset", db_field.remote_field.model.objects)
            kwargs["queryset"] = qs.select_related("content_type")
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)

    # ---- Permissions ----
    def has_delete_permission(self, request, customer=None):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True
