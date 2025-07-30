from django.contrib import admin

from apps.appInfo.models.contact_us import ContactUs
from common.base.admin import BaseModelAdmin

from .change_view import ContactUsChangeView
from .display import ContactUsDisplayMixin
from .list_view import ContactUsListView
from .permissions import ContactUsAdminPermissions


@admin.register(ContactUs)
class ContactUsAdmin(
    ContactUsDisplayMixin,
    ContactUsListView,
    ContactUsChangeView,
    ContactUsAdminPermissions,
    BaseModelAdmin,
):
    inlines = []
