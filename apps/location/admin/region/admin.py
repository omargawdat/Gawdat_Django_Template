from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.location.models.region import Region
from common.base.admin import BaseModelAdmin

from .change_view import RegionChangeView
from .display import RegionDisplayMixin
from .list_view import RegionListView
from .permissions import RegionAdminPermissions


@admin.register(Region)
class RegionAdmin(
    RegionDisplayMixin,
    RegionListView,
    RegionChangeView,
    RegionAdminPermissions,
    BaseModelAdmin,
    TabbedTranslationAdmin,
):
    pass
