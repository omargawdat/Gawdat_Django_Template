import json
from secrets import SystemRandom
from typing import Any

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


def dashboard_callback(request, context: dict[str, Any]) -> dict[str, Any]:
    weekdays = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    secure_random = SystemRandom()

    # Refactored to avoid boolean parameters
    def generate_positive_data_points(start: int, end: int):
        return [[1, secure_random.randrange(8, 28)] for _ in range(start, end)]

    def generate_negative_data_points(start: int, end: int):
        return [[-1, -secure_random.randrange(8, 28)] for _ in range(start, end)]

    positive = generate_positive_data_points(1, 28)
    negative = generate_negative_data_points(1, 28)
    average = [r[1] - secure_random.randint(3, 5) for r in positive]
    performance_positive = generate_positive_data_points(1, 28)
    performance_negative = generate_negative_data_points(1, 28)

    def generate_metric():
        return f"${intcomma(f'{secure_random.uniform(1000, 9999):.02f}')}"

    def format_progress_footer(value: float):
        return format_html(
            '<strong class="text-green-700 font-semibold dark:text-green-400">+{}%</strong>&nbsp;progress from last week',
            intcomma(f"{secure_random.uniform(1, 9):.02f}"),
        )

    context.update(
        {
            "navigation": [
                {"title": _("Dashboard"), "link": "/", "active": True},
                {"title": _("Analytics"), "link": "#"},
                {"title": _("Settings"), "link": "#"},
            ],
            "filters": [
                {"title": _("All"), "link": "#", "active": True},
                {"title": _("New"), "link": "#"},
            ],
            "kpi": [
                {
                    "title": "Product A Performance",
                    "metric": generate_metric(),
                    "footer": format_progress_footer(secure_random.uniform(1, 9)),
                    "chart": json.dumps(
                        {
                            "labels": [weekdays[day % 7] for day in range(1, 28)],
                            "datasets": [{"data": average, "borderColor": "#9333ea"}],
                        },
                    ),
                },
                {
                    "title": "Product B Performance",
                    "metric": generate_metric(),
                    "footer": format_progress_footer(secure_random.uniform(1, 9)),
                },
                {
                    "title": "Product C Performance",
                    "metric": generate_metric(),
                    "footer": format_progress_footer(secure_random.uniform(1, 9)),
                },
            ],
            "progress": [
                {
                    "title": title,
                    "description": generate_metric(),
                    "value": secure_random.randint(10, 90),
                }
                for title in [
                    "🦆 Social marketing e-book",
                    "🦍 Freelancing tasks",
                    "🐋 Development coaching",
                    "🦑 Product consulting",
                    "🐨 Other income",
                    "🐶 Course sales",
                    "🐻‍❄️ Ads revenue",
                    "🦩 Customer Retention Rate",
                    "🦊 Marketing ROI",
                    "🦁 Affiliate partnerships",
                ]
            ],
            "chart": json.dumps(
                {
                    "labels": [weekdays[day % 7] for day in range(1, 28)],
                    "datasets": [
                        {
                            "label": "Example 1",
                            "type": "line",
                            "data": average,
                            "backgroundColor": "#f0abfc",
                            "borderColor": "#f0abfc",
                        },
                        {
                            "label": "Example 2",
                            "data": positive,
                            "backgroundColor": "#9333ea",
                        },
                        {
                            "label": "Example 3",
                            "data": negative,
                            "backgroundColor": "#f43f5e",
                        },
                    ],
                },
            ),
            "performance": [
                {
                    "title": _("Last week revenue"),
                    "metric": "$1,234.56",
                    "footer": format_html(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week',
                    ),
                    "chart": json.dumps(
                        {
                            "labels": [weekdays[day % 7] for day in range(1, 28)],
                            "datasets": [
                                {
                                    "data": performance_positive,
                                    "borderColor": "#9333ea",
                                },
                            ],
                        },
                    ),
                },
                {
                    "title": _("Last week expenses"),
                    "metric": "$1,234.56",
                    "footer": format_html(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week',
                    ),
                    "chart": json.dumps(
                        {
                            "labels": [weekdays[day % 7] for day in range(1, 28)],
                            "datasets": [
                                {
                                    "data": performance_negative,
                                    "borderColor": "#f43f5e",
                                },
                            ],
                        },
                    ),
                },
            ],
        },
    )

    return context
