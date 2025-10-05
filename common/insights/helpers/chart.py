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

    @staticmethod
    def format_line_chart_data() -> dict[str, dict[str, dict[str, list]]]:
        """Generate chart data using real payment data from database"""

        # Get real payment data
        monthly_data = InsightSelector.get_monthly_payment_data()
        yearly_data = InsightSelector.get_yearly_payment_data()

        payments_sessions_data = {
            "payments": {
                "monthly": {
                    "labels": monthly_data["labels"],
                    "datasets": [
                        {
                            "type": "line",
                            "data": monthly_data["amounts"],
                            "borderColor": "#10b981",
                            "pointBorderColor": "#10b981",
                            "pointBackgroundColor": "#10b981",
                        }
                    ],
                },
                "yearly": {
                    "labels": yearly_data["labels"],
                    "datasets": [
                        {
                            "type": "line",
                            "data": yearly_data["amounts"],
                            "borderColor": "#10b981",
                            "pointBorderColor": "#10b981",
                            "pointBackgroundColor": "#10b981",
                        }
                    ],
                },
            },
            "orders": {
                "monthly": {
                    "labels": monthly_data["labels"],
                    "datasets": [
                        {
                            "type": "line",
                            "data": monthly_data["counts"],
                            "borderColor": "#6366f1",
                            "pointBorderColor": "#6366f1",
                            "pointBackgroundColor": "#6366f1",
                        }
                    ],
                },
                "yearly": {
                    "labels": yearly_data["labels"],
                    "datasets": [
                        {
                            "type": "line",
                            "data": yearly_data["counts"],
                            "borderColor": "#6366f1",
                            "pointBorderColor": "#6366f1",
                            "pointBackgroundColor": "#6366f1",
                        }
                    ],
                },
            },
        }
        return payments_sessions_data
