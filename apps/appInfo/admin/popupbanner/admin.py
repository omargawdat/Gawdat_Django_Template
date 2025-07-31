from django.contrib import admin

from apps.appInfo.models.popup import PopUpBanner
from common.base.admin import BaseModelAdmin

from .change_view import PopUpBannerChangeView
from .display import PopUpBannerDisplayMixin
from .list_view import PopUpBannerListView
from .permissions import PopUpBannerAdminPermissions


@admin.register(PopUpBanner)
class PopUpBannerAdmin(
    PopUpBannerDisplayMixin,
    PopUpBannerListView,
    PopUpBannerChangeView,
    PopUpBannerAdminPermissions,
    BaseModelAdmin,
):
    inlines = []
