from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.channel.admin.notification.change_view import NotificationChangeView
from apps.channel.admin.notification.display import NotificationDisplayMixin
from apps.channel.admin.notification.list_view import NotificationListView
from apps.channel.admin.notification.permissions import NotificationAdminPermissions
from apps.channel.models.notification import Notification
from common.base.admin import BaseModelAdmin


@admin.register(Notification)
class NotificationAdmin(
    NotificationDisplayMixin,
    NotificationListView,
    NotificationChangeView,
    NotificationAdminPermissions,
    TabbedTranslationAdmin,
    BaseModelAdmin,
):
    pass
