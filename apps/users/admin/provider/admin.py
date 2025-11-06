from django.contrib import admin

from apps.users.models.provider import Provider
from common.base.admin import BaseModelAdmin

from .change_view import ProviderChangeView
from .display import ProviderDisplayMixin
from .list_view import ProviderListView
from .permissions import ProviderAdminPermissions


@admin.register(Provider)
class ProviderAdmin(
    ProviderDisplayMixin,
    ProviderListView,
    ProviderChangeView,
    ProviderAdminPermissions,
    BaseModelAdmin,
):
    pass
