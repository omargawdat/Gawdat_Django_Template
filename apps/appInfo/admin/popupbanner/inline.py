from apps.appInfo.models.popup import PopUpBanner
from common.base.admin import BaseTabularInline

from .permissions import PopUpBannerInlinePermissions


class PopUpBannerInline(PopUpBannerInlinePermissions, BaseTabularInline):
    model = PopUpBanner
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
