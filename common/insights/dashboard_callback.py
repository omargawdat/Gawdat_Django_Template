from typing import Any

from django.utils.translation import gettext_lazy as _

from common.insights.helpers.chart import ChartHelper
from common.insights.selectors.insight_selector import InsightSelector


def dashboard_callback(request, context: dict[str, Any]) -> dict[str, Any]:
    # Build context using chart helpers
    context.update(
        {
            "navigation": [
                {"title": _("Analytics"), "link": "#", "active": True},
            ],
            "kpi": ChartHelper.get_kpi_data(),
            "social_accounts": InsightSelector.get_social_accounts(),
        }
    )

    return context
