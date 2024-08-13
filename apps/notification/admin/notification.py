from django.contrib import admin
from django.forms import ModelForm
from django.shortcuts import redirect
from django.urls import path

from apps.notification.models.notification import Notification
from common.base.basemodeladmin import BaseModelAdmin


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = "__all__"


@admin.register(Notification)
class NotificationAdmin(BaseModelAdmin):
    #  List View
    # -----------------------------------------------------------------------------------------

    # Change View
    # -----------------------------------------------------------------------------------------
    form = NotificationForm

    def get_fieldsets(self, request, obj=None):
        return ((None, {"fields": ("title", "message_body", "users")}),)

    def get_readonly_fields(self, request, obj=None):
        return ()

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "add/",
                self.admin_site.admin_view(self.add_view),
                name="notification_notification_add",
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        return redirect("admin:notification_notification_add")

    # Permissions
    # -----------------------------------------------------------------------------------------
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
