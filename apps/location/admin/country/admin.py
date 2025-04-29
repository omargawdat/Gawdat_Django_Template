from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.location.models.country import Country
from common.base.admin import BaseModelAdmin

from .change_view import CountryChangeView
from .display import CountryDisplayMixin
from .list_view import CountryListView
from .permissions import CountryAdminPermissions


@admin.register(Country)
class CountryAdmin(
    CountryDisplayMixin,
    CountryListView,
    CountryChangeView,
    CountryAdminPermissions,
    TabbedTranslationAdmin,  # todo: bug not showing the name !!
    BaseModelAdmin,
):
    pass
