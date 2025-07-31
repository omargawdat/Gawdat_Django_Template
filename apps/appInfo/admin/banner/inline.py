from apps.appInfo.models.banner import Banner
from common.base.admin import BaseTabularInline

from .permissions import BannerInlinePermissions


class BannerInline(BannerInlinePermissions, BaseTabularInline):
    model = Banner
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
