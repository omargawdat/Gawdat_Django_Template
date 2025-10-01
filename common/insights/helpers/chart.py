from common.insights.selectors.insight_selector import InsightSelector


class ChartHelper:
    """Helper class for generating chart configurations."""

    @staticmethod
    def get_kpi_data() -> list[dict]:
        """Generate KPI cards data."""
        revenue_data = InsightSelector.get_total_revenue()
        customers_count = InsightSelector.get_total_active_customer()
        orders_count = InsightSelector.get_total_paid_orders()

        return [
            {
                "title": "Total Customers",
                "metric": customers_count,
                "display": str(customers_count),
            },
            {
                "title": "TOTAL Revenue",
                "metric": revenue_data["value"],
                "display": revenue_data["display"],
            },
            {
                "title": "TOTAL Orders",
                "metric": orders_count,
                "display": str(orders_count),
            },
        ]
