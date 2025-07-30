from apps.appInfo.models.contact_us import ContactUs
from common.base.admin import BaseTabularInline

from .permissions import ContactUsInlinePermissions


class ContactUsInline(ContactUsInlinePermissions, BaseTabularInline):
    model = ContactUs
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
