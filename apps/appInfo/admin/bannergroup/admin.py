from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

# from apps.appInfo.admin.banner.inline import BannerInline
from apps.appInfo.models.banner_group import BannerGroup
from common.base.admin import BaseModelAdmin

from .change_view import BannerGroupChangeView
from .display import BannerGroupDisplayMixin
from .list_view import BannerGroupListView
from .permissions import BannerGroupAdminPermissions


@admin.register(BannerGroup)
class BannerGroupAdmin(
    BannerGroupDisplayMixin,
    BannerGroupListView,
    BannerGroupChangeView,
    BannerGroupAdminPermissions,
    BaseModelAdmin,
    TabbedTranslationAdmin,
):
    # inlines = [BannerInline]
    pass
