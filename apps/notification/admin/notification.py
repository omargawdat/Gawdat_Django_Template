from django.contrib import admin
from django.forms import ModelForm
from django.shortcuts import redirect
from django.urls import path
from unfold.admin import ModelAdmin

from apps.notification.models.notification import Notification
from common.mixins.pass_request_to_form import RequestFormMixin


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ["title", "message_body", "users"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        readonly_fields = kwargs.pop("readonly_fields", [])
        print("readonly_fields:", readonly_fields)  # noqa T201
        super().__init__(*args, **kwargs)


@admin.register(Notification)
class NotificationAdmin(RequestFormMixin, ModelAdmin):
    form = NotificationForm
    readonly_fields = ("message_body",)

    fieldsets = ((None, {"fields": ("title", "message_body", "users")}),)
    filter_horizontal = ("users",)

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
