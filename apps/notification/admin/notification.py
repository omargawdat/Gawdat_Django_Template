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
        fields = "__all__"

    def clean_title(self):
        return self.cleaned_data["title"].upper()


@admin.register(Notification)
class NotificationAdmin(RequestFormMixin, ModelAdmin):
    form = NotificationForm
    readonly_fields = ("message_body",)

    fieldsets = ((None, {"fields": ("users", "title", "message_body")}),)
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
