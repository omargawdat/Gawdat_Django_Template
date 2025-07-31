from apps.appInfo.models.banner_group import BannerGroup
from common.base.admin import BaseTabularInline

from .permissions import BannerGroupInlinePermissions


class BannerGroupInline(BannerGroupInlinePermissions, BaseTabularInline):
    model = BannerGroup
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
