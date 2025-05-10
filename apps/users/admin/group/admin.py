from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    filter_horizontal = ("permissions",)
    list_display = ("name",)
    search_fields = ("name",)
    search_help_text = _("Search by group name...🔍")
    ordering = ("name",)
