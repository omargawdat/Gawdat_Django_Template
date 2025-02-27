# type: ignore
# ruff: noqa

import secrets

from django.utils.timezone import now
from django.utils.timezone import timedelta
from unfold.components import BaseComponent
from unfold.components import register_component

# Constants
MIN_COLOR_VALUE = 2
MAX_COLOR_VALUE = 6
THRESHOLD_COLOR_INDEX = 4
GRID_SIZE = 72
GROUP_COUNT = 10
PROBABILITY_THRESHOLD = 4


@register_component
class TrackerComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []

        # Fixed B007: Changed i to _ since loop variable isn't used
        # Fixed S311: Using secrets for cryptographic randomness
        for _ in range(1, GRID_SIZE):
            # Using getrandbits for boolean choice
            has_value = secrets.randbelow(5) < PROBABILITY_THRESHOLD
            color = None
            tooltip = None
            if has_value:
                value = MIN_COLOR_VALUE + secrets.randbelow(
                    MAX_COLOR_VALUE - MIN_COLOR_VALUE + 1
                )
                color = f"bg-primary-{value}00 dark:bg-primary-{9 - value}00"
                tooltip = f"Value {value}"

            data.append(
                {
                    "color": color,
                    "tooltip": tooltip,
                }
            )

        context["data"] = data
        return context


@register_component
class CohortComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = []
        headers = []
        cols = []

        dates = reversed(
            [(now() - timedelta(days=x)).strftime("%B %d, %Y") for x in range(8)]
        )
        groups = range(1, GROUP_COUNT)

        for row_index, date in enumerate(dates):
            cols = []

            for col_index, _col in enumerate(groups):
                color_index = 8 - row_index - col_index
                col_classes = []

                if color_index > 0:
                    col_classes.append(
                        f"bg-primary-{color_index}00 dark:bg-primary-{9 - color_index}00"
                    )

                # Fixed PLR2004: Using constant instead of magic number
                if color_index >= THRESHOLD_COLOR_INDEX:
                    col_classes.append("text-white dark:text-gray-600")

                # Fixed S311: Using secrets for random values
                base_value = 4000 - (col_index * row_index * 225)
                range_size = 1000
                value = base_value + secrets.randbelow(range_size)

                # Fixed S311: Using secrets for percentage
                subtitle = f"{10 + secrets.randbelow(91)}%"

                if value <= 0:
                    value = 0
                    subtitle = None

                cols.append(
                    {
                        "value": value,
                        "color": " ".join(col_classes),
                        "subtitle": subtitle,
                    }
                )

            rows.append(
                {
                    "header": {
                        "title": date,
                        "subtitle": f"Total {sum(col['value'] for col in cols):,}",
                    },
                    "cols": cols,
                }
            )

        for index, group in enumerate(groups):
            total = sum(row["cols"][index]["value"] for row in rows)

            headers.append(
                {
                    "title": f"Group #{group}",
                    "subtitle": f"Total {total:,}",
                }
            )

        context["data"] = {
            "headers": headers,
            "rows": rows,
        }

        return context
