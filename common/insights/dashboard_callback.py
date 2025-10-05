import json
from typing import Any

from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money

from apps.appInfo.models.contact_us import ContactUs
from common.insights.helpers.chart import ChartHelper
from common.insights.selectors.insight_selector import InsightSelector


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
