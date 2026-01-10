from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import XLSX
from unfold.contrib.import_export.forms import ExportForm

from apps.users.admin.provider.resource import ProviderResource
from apps.users.domain.selectors.provider import ProviderSelector
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
    ExportActionModelAdmin,
    BaseModelAdmin,
):
    resource_class = ProviderResource
    export_form_class = ExportForm
    formats = [XLSX]
    change_list_template = "admin/users/provider/change_list.html"
    import_export_change_list_template = "admin/users/provider/change_list.html"

    def changelist_view(self, request, extra_context=None):
        avg_orders = ProviderSelector.get_avg_orders_per_provider()
        avg_revenue = ProviderSelector.get_avg_revenue_per_provider()
        total_providers_today = ProviderSelector.get_providers_joined_today()
        top_rated_percentage = ProviderSelector.get_top_rated_providers_percentage()

        cards = [
            {
                "title": _("Avg Orders Per Provider"),
                "value": avg_orders,
                "description": _("Average number of orders per provider"),
            },
            {
                "title": _("Avg Revenue Per Provider"),
                "value": avg_revenue,
                "description": _("Average revenue earned by each provider"),
            },
            {
                "title": _("Providers Joined Today"),
                "value": total_providers_today,
                "description": _("Number of new providers who signed up today"),
            },
            {
                "title": _("Top Rated Providers"),
                "value": top_rated_percentage,
                "description": _("Percentage of providers with rating above 4.5"),
            },
        ]

        extra_context = extra_context or {}
        extra_context.update(
            {
                "provider_cards": cards,
            }
        )
        return super().changelist_view(request, extra_context=extra_context)
