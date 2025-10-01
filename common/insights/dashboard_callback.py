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


def get_unread_contacts():
    unread_qs = (
        ContactUs.objects.select_related("customer")
        .filter(has_checked=False)
        .order_by("-created_at")
    )
    unread_contacts = [
        {
            "id": c.id,
            "customer_name": f"{c.customer.full_name}",
            "customer_phone": c.customer.phone_number,
            "description": c.description,
            "created_at": c.created_at.strftime("%b %d, %Y %H:%M"),
        }
        for c in unread_qs
    ]
    return unread_contacts, unread_qs.count()


def get_social_account():
    from apps.appInfo.models.social import SocialAccount

    return SocialAccount.get_solo()


def get_kpi(total_orders, total_bookings, total_egp, total_sar):
    return [
        {
            "title": "Total Orders 🛒",
            "metric": total_orders if total_orders is not None else 0,
        },
        {
            "title": "Total Booking 🗓️",
            "metric": total_bookings if total_bookings is not None else 0,
        },
        {
            "title": "Total Payment (EGP) 💰",
            "metric": total_egp,
        },
        {
            "title": "Total Payment (SAR) 💰",
            "metric": total_sar,
        },
    ]


def get_progress(names, orders):
    return [
        {
            "title": f"🏢 {index + 1}. {name}",
            "description": f"{order} Orders 🛍️",
            "value": order,
        }
        for index, (name, order) in enumerate(zip(names, orders, strict=False))
    ]


def get_chart(labels_daily, get_order_last_month):
    return json.dumps(
        {
            "labels": labels_daily,
            "datasets": [
                {
                    "label": "Orders",
                    "type": "bar",
                    "data": get_order_last_month(),
                    "backgroundColor": "#f0abfc",
                    "borderColor": "#f0abfc",
                },
            ],
        }
    )


def get_customer_growth_chart(
    labels_month, customer_growth_daily, labels_year, customer_growth_monthly
):
    return json.dumps(
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
    )


def get_performance(labels_daily, revenue_egp_daily, revenue_sar_daily):
    return [
        {
            "title": _("Last Month Revenue in Egypt"),
            "metric": Money(sum(revenue_egp_daily), "EGP"),
            "footer": format_html(
                '{}<strong class="text-green-600 font-medium">+3.14%</strong> vs last week',
                "",
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
            "metric": Money(sum(revenue_sar_daily), "SAR"),
            "footer": format_html(
                '{}<strong class="text-green-600 font-medium">+3.14%</strong> vs last week',
                "",
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
    ]


def dashboard_callback(request, context: dict[str, Any]) -> dict[str, Any]:
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    growth = get_customer_growth_data()
    labels_month = growth["daily"]["labels"]
    customer_growth_daily = growth["daily"]["data"]
    labels_year = growth["yearly"]["labels"]
    customer_growth_monthly = growth["yearly"]["data"]

    providers_with_most_orders = None

    def get_order_counts():
        if providers_with_most_orders:
            return [provider.order_count for provider in providers_with_most_orders]
        return []

    def get_names():
        if providers_with_most_orders:
            return [provider.full_name for provider in providers_with_most_orders]
        return []

    names = get_names()
    orders = get_order_counts()
    total_orders = None
    total_bookings = None

    def get_total_earnings(currency):
        earnings = None
        total = earnings["total"] if earnings and earnings["total"] else Decimal("0")
        return Money(total, currency)

    total_sar = get_total_earnings("SAR")
    total_egp = get_total_earnings("EGP")

    def get_total_revenue_last_month(currency):
        today = timezone.now().date()
        last_month_start = today - timezone.timedelta(days=29)
        revenue_per_day = None
        revenue_dict_daily = (
            {entry["day"]: float(entry["total"]) for entry in revenue_per_day}
            if revenue_per_day
            else {}
        )
        date_list = [last_month_start + timezone.timedelta(days=i) for i in range(30)]
        daily_revenue = [revenue_dict_daily.get(date, 0.0) for date in date_list]
        return daily_revenue

    revenue_egp_daily = get_total_revenue_last_month("EGP")
    revenue_sar_daily = get_total_revenue_last_month("SAR")

    def get_order_last_month():
        today = timezone.now().date()
        last_month_start = today - timezone.timedelta(days=29)
        orders_per_day = None
        orders_dict_daily = (
            {entry["day"]: entry["count"] for entry in orders_per_day}
            if orders_per_day
            else {}
        )
        date_list = [last_month_start + timezone.timedelta(days=i) for i in range(30)]
        daily_orders = [orders_dict_daily.get(date, 0) for date in date_list]
        return daily_orders

    today = timezone.now().date()
    last_month_start = today - timezone.timedelta(days=29)
    date_list = [last_month_start + timezone.timedelta(days=i) for i in range(30)]
    labels_daily = [weekdays[date.weekday()] for date in date_list]

    unread_contacts, unread_contacts_count = get_unread_contacts()
    social_account = get_social_account()

    context.update(
        {
            "navigation": [
                {"title": _("Analytics"), "link": "#", "active": True},
            ],
            "unread_contacts": unread_contacts,
            "unread_contacts_count": unread_contacts_count,
            "kpi": get_kpi(total_orders, total_bookings, total_egp, total_sar),
            "progress": get_progress(names, orders),
            "chart": get_chart(labels_daily, get_order_last_month),
            "customer_growth_chart": get_customer_growth_chart(
                labels_month,
                customer_growth_daily,
                labels_year,
                customer_growth_monthly,
            ),
            "performance": get_performance(
                labels_daily, revenue_egp_daily, revenue_sar_daily
            ),
            "social_account": social_account,
        }
    )
    return context
