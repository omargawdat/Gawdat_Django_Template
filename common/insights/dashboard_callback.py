from typing import Any

from django.utils.translation import gettext_lazy as _

# Import selectors
# Import helpers
from common.insights.helpers.chart import ChartHelper


def dashboard_callback(request, context: dict[str, Any]) -> dict[str, Any]:
    # Build context using chart helpers
    context.update(
        {
            "navigation": [
                {"title": _("Analytics"), "link": "#", "active": True},
            ],
            "kpi": ChartHelper.get_kpi_data(),
        }
    )

    return context
