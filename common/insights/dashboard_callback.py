import json
from decimal import Decimal
from typing import Any

from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from moneyed import Money

from apps.appInfo.models.contact_us import ContactUs


def get_customer_growth_data():
    """Return daily and yearly customer growth data and labels."""
    import calendar
    from collections import Counter

    from apps.users.models.customer import Customer

    today = timezone.now().date()
    # Daily (current month)
    first_day_of_month = today.replace(day=1)
    num_days = (today - first_day_of_month).days + 1
    date_list_month = [
        first_day_of_month + timezone.timedelta(days=i) for i in range(num_days)
    ]
    customers_this_month = Customer.objects.filter(
        date_joined__date__gte=first_day_of_month, date_joined__date__lte=today
    )
    joined_per_day = Counter(c.date_joined.date() for c in customers_this_month)
    customer_growth_daily = [joined_per_day.get(day, 0) for day in date_list_month]
    labels_month = [day.strftime("%b %-d") for day in date_list_month]
    # Yearly (per month)
    first_day_of_year = today.replace(month=1, day=1)
    customers_this_year = Customer.objects.filter(
        date_joined__date__gte=first_day_of_year, date_joined__date__lte=today
    )
    joined_per_month = Counter(
        (c.date_joined.year, c.date_joined.month) for c in customers_this_year
    )
    customer_growth_monthly = [
        joined_per_month.get((today.year, m), 0) for m in range(1, 13)
    ]
    labels_year = [calendar.month_abbr[m] for m in range(1, 13)]
    return {
        "daily": {"labels": labels_month, "data": customer_growth_daily},
        "yearly": {"labels": labels_year, "data": customer_growth_monthly},
    }


def dashboard_callback(request, context: dict[str, Any]) -> dict[str, Any]:
    # Weekday labels for charts, used to display day names in charts (e.g., "Mon", "Tue")
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # --- Customer growth for the current month and year ---
    growth = get_customer_growth_data()
    labels_month = growth["daily"]["labels"]
    customer_growth_daily = growth["daily"]["data"]
    labels_year = growth["yearly"]["labels"]
    customer_growth_monthly = growth["yearly"]["data"]

    # Placeholder for providers with the most orders
    # This should be replaced with an actual queryset, e.g., Provider.objects.annotate(order_count=Count('orders')).order_by('-order_count')[:10]
    providers_with_most_orders = None

    def get_order_counts():
        """Extract order counts from the providers_with_most_orders queryset. Returns an empty list if no data is available."""
        if providers_with_most_orders:
            return [provider.order_count for provider in providers_with_most_orders]
        return []

    def get_names():
        """Extract full names from the providers_with_most_orders queryset. Returns an empty list if no data is available."""
        if providers_with_most_orders:
            return [provider.full_name for provider in providers_with_most_orders]
        return []

    # Fetch names and order counts for top providers
    names = get_names()
    orders = get_order_counts()

    # Placeholder for total orders count
    # Replace with an actual queryset, e.g., Order.objects.count()
    total_orders = None

    # Placeholder for total bookings count
    # Replace with an actual queryset, e.g., BookingRequest.objects.count()
    total_bookings = None

    def get_total_earnings(currency):
        """Calculate total earnings in the specified currency. Returns Money(0, currency) if no data is available."""
        # Placeholder for earnings aggregate
        # Replace with an actual queryset, e.g., Order.objects.filter(payment__base_amount_currency=currency).aggregate(total=Sum("payment__base_amount"))
        earnings = None
        total = earnings["total"] if earnings and earnings["total"] else Decimal("0")
        return Money(total, currency)

    # Calculate total earnings in SAR and EGP currencies
    total_sar = get_total_earnings("SAR")
    total_egp = get_total_earnings("EGP")

    def get_total_revenue_last_month(currency):
        """Retrieve daily revenue for the last 30 days in the specified currency. Returns a list of daily values, defaulting to 0.0 for missing days."""
        today = timezone.now().date()
        last_month_start = today - timezone.timedelta(days=29)
        # Placeholder for revenue per day
        # Replace with an actual queryset, e.g., Order.objects.filter(...).annotate(day=TruncDate('created_at')).values('day').annotate(total=Sum('payment__base_amount'))
        revenue_per_day = None
        revenue_dict_daily = (
            {entry["day"]: float(entry["total"]) for entry in revenue_per_day}
            if revenue_per_day
            else {}
        )
        date_list = [last_month_start + timezone.timedelta(days=i) for i in range(30)]
        daily_revenue = [revenue_dict_daily.get(date, 0.0) for date in date_list]
        return daily_revenue

    # Get daily revenue for the last 30 days in EGP and SAR
    revenue_egp_daily = get_total_revenue_last_month("EGP")
    revenue_sar_daily = get_total_revenue_last_month("SAR")

    def get_order_last_month():
        """Retrieve daily order counts for the last 30 days. Returns a list of counts, defaulting to 0 for missing days."""
        today = timezone.now().date()
        last_month_start = today - timezone.timedelta(days=29)
        # Placeholder for orders per day
        # Replace with an actual queryset, e.g., Order.objects.filter(...).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id'))
        orders_per_day = None
        orders_dict_daily = (
            {entry["day"]: entry["count"] for entry in orders_per_day}
            if orders_per_day
            else {}
        )
        date_list = [last_month_start + timezone.timedelta(days=i) for i in range(30)]
        daily_orders = [orders_dict_daily.get(date, 0) for date in date_list]
        return daily_orders

    # Prepare date labels for the last 30 days using weekday names (e.g., "Mon", "Tue")
    today = timezone.now().date()
    last_month_start = today - timezone.timedelta(days=29)
    date_list = [last_month_start + timezone.timedelta(days=i) for i in range(30)]
    labels_daily = [weekdays[date.weekday()] for date in date_list]

    # Get recent contact messages (last 5 messages)
    contact_messages = ContactUs.objects.select_related("customer").order_by(
        "-created_at"
    )[:5]
    total_messages_count = ContactUs.objects.count()

    # Get social accounts (singleton)
    from apps.appInfo.models.social import SocialAccount

    social_account = SocialAccount.get_solo()

    # Update the context dictionary with data for the dashboard template
    context.update(
        {
            # Navigation menu item for the dashboard
            "navigation": [
                {"title": _("Analytics"), "link": "#", "active": True},
            ],
            # Contact messages for the dashboard
            "contact_messages": contact_messages,
            "total_messages_count": total_messages_count,
            # Key Performance Indicators (KPIs) for display
            "kpi": [
                {
                    "title": "Total Orders 🛒",
                    "metric": total_orders
                    if total_orders is not None
                    else 0,  # Default to 0 if no data
                },
                {
                    "title": "Total Booking 🗓️",
                    "metric": total_bookings
                    if total_bookings is not None
                    else 0,  # Default to 0 if no data
                },
                {
                    "title": "Total Payment (EGP) 💰",
                    "metric": total_egp,
                },
                {
                    "title": "Total Payment (SAR) 💰",
                    "metric": total_sar,
                },
            ],
            # Progress indicators showing top providers and their order counts
            "progress": [
                {
                    "title": f"🏢 {index + 1}. {name}",
                    "description": f"{order} Orders 🛍️",
                    "value": order,  # Required for progress component in the template
                }
                for index, (name, order) in enumerate(zip(names, orders, strict=False))
            ],
            # Chart data for displaying orders over the last 30 days
            "chart": json.dumps(
                {
                    "labels": labels_daily,
                    "datasets": [
                        {
                            "label": "Orders",
                            "type": "bar",  # Specifies a bar chart type for the template
                            "data": get_order_last_month(),
                            "backgroundColor": "#f0abfc",
                            "borderColor": "#f0abfc",
                        },
                    ],
                }
            ),
            # Chart data for customer growth (per day and per year)
            "customer_growth_chart": json.dumps(
                {
                    "daily": {
                        "labels": labels_month,
                        "datasets": [
                            {
                                "label": "New Customers (Daily)",
                                "type": "line",
                                "data": customer_growth_daily,
                                "borderColor": "#4ade80",
                                "backgroundColor": "rgba(74,222,128,0.2)",
                                "fill": True,
                                "tension": 0.4,
                            },
                        ],
                    },
                    "yearly": {
                        "labels": labels_year,
                        "datasets": [
                            {
                                "label": "New Customers (Monthly)",
                                "type": "line",
                                "data": customer_growth_monthly,
                                "borderColor": "#9333ea",
                                "backgroundColor": "rgba(147,51,234,0.15)",
                                "fill": True,
                                "tension": 0.4,
                            },
                        ],
                    },
                }
            ),
            # Performance metrics for revenue in Egypt and Saudi Arabia over the last 30 days
            "performance": [
                {
                    "title": _("Last Month Revenue in Egypt"),
                    "metric": Money(
                        sum(revenue_egp_daily), "EGP"
                    ),  # Sum of daily revenue
                    "footer": format_html(
                        '<strong class="text-green-600 font-medium">+3.14%</strong> vs last week'
                        # Static comparison text
                    ),
                    "chart": json.dumps(
                        {
                            "labels": labels_daily,
                            "datasets": [
                                {
                                    "data": revenue_egp_daily,
                                    "borderColor": "#9333ea",
                                },
                            ],
                        }
                    ),
                },
                {
                    "title": _("Last Month Revenue in Saudi Arabia"),
                    "metric": Money(
                        sum(revenue_sar_daily), "SAR"
                    ),  # Sum of daily revenue
                    "footer": format_html(
                        '<strong class="text-green-600 font-medium">+3.14%</strong> vs last week'
                        # Static comparison text
                    ),
                    "chart": json.dumps(
                        {
                            "labels": labels_daily,
                            "datasets": [
                                {
                                    "data": revenue_sar_daily,
                                    "borderColor": "#9333ea",
                                },
                            ],
                        }
                    ),
                },
            ],
            # Social account for display in the dashboard
            "social_account": social_account,
        }
    )

    return context
