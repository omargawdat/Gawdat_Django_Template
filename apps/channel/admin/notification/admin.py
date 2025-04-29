from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.channel.models.notification import Notification
from common.base.admin import BaseModelAdmin

from .change_view import NotificationChangeView
from .display import NotificationDisplayMixin
from .list_view import NotificationListView
from .permissions import NotificationAdminPermissions


@admin.register(Notification)
class NotificationAdmin(
    NotificationDisplayMixin,
    NotificationListView,
    NotificationChangeView,
    NotificationAdminPermissions,
    BaseModelAdmin,
    TabbedTranslationAdmin,
):
    pass
