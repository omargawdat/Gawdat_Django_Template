from django.contrib import admin

from apps.appInfo.models.banner import Banner
from common.base.admin import BaseModelAdmin

from .change_view import BannerChangeView
from .display import BannerDisplayMixin
from .list_view import BannerListView
from .permissions import BannerAdminPermissions


@admin.register(Banner)
class BannerAdmin(
    BannerDisplayMixin,
    BannerListView,
    BannerChangeView,
    BannerAdminPermissions,
    BaseModelAdmin,
):
    inlines = []
