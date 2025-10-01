import json
from typing import Any

from django.utils.translation import gettext_lazy as _

from common.insights.helpers.chart import ChartHelper
from common.insights.selectors.insight_selector import InsightSelector


def dashboard_callback(request, context: dict[str, Any]) -> dict[str, Any]:
    # Get unchecked contacts
    unread_contacts = InsightSelector.get_unchecked_contacts(limit=10)
    unread_contacts_count = len(unread_contacts)

    # Build context using chart helpers
    context.update(
        {
            "navigation": [
                {"title": _("Analytics"), "link": "#", "active": True},
            ],
            "kpi": ChartHelper.get_kpi_data(),
            "payments_orders_chart": json.dumps(ChartHelper.format_line_chart_data()),
            "social_accounts": InsightSelector.get_social_accounts(),
            "unread_contacts": unread_contacts,
            "unread_contacts_count": unread_contacts_count,
        }
    )

    return context
