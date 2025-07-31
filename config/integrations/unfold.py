from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from config.helpers.env import env

UNFOLD = {
    "SITE_TITLE": "projectname Dashboard",
    "SITE_HEADER": "projectname",
    "SHOW_HISTORY": True,
    "SHOW_LANGUAGES": True,
    "SHOW_BACK_BUTTON": True,
    "SITE_URL": "https://www.google.com/",  # todo: set this to the actual site url
    "LOGIN": {
        "image": lambda request: static("images/logo.png"),
    },
    "STYLES": [
        lambda request: static("css/style.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/script.js"),
    ],
    "SITE_SYMBOL": "anchor",
    "SITE_ICON": {
        "light": lambda request: get_site_icon(request),
        "dark": lambda request: get_site_icon(request),
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "48x48",
            "type": "image/svg+xml",
            "href": lambda request: static("images/identity.png"),
        },
    ],
    "ENVIRONMENT": lambda request: environment_callback(request),
    "ENVIRONMENT_TITLE_PREFIX": env.environment,
    "DASHBOARD_CALLBACK": "common.insights.dashboard_callback.dashboard_callback",
    "BORDER_RADIUS": "8px",
    "COLORS": {
        "base": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
        "primary": {
            "50": "240 253 244",
            "100": "220 252 231",
            "200": "187 247 208",
            "300": "134 239 172",
            "400": "74 222 128",
            "500": "34 197 94",
            "600": "22 163 74",
            "700": "21 128 61",
            "800": "22 101 52",
            "900": "20 83 45",
            "950": "5 46 22",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "ar": "🇸🇦",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Users 👥"),
                "separator": True,
                "items": [
                    {
                        "title": _("Customer"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_customer_changelist"),
                        "badge": "config.integrations.unfold.badge_customers_week_count",
                        "permission": lambda request: request.user.has_perm(
                            "users.view_customer"
                        ),
                    },
                    {
                        "title": _("Admin"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_adminuser_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "users.view_adminuser"
                        ),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "auth.view_group"
                        ),
                    },
                    {
                        "title": _("Notification"),
                        "icon": "notifications",
                        "link": reverse_lazy("admin:channel_notification_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "channel.view_notification"
                        ),
                    },
                ],
            },
            {
                "title": _("Payment 💳"),
                "separator": True,
                "items": [
                    {
                        "title": _("Wallet"),
                        "icon": "wallet",
                        "link": reverse_lazy("admin:payment_wallet_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "payment.view_wallet"
                        ),
                    },
                    {
                        "title": _("Wallet Transaction"),
                        "icon": "account_balance_wallet",
                        "link": reverse_lazy(
                            "admin:payment_wallettransaction_changelist"
                        ),
                        "permission": lambda request: request.user.has_perm(
                            "payment.view_wallettransaction"
                        ),
                    },
                ],
            },
            {
                "title": _("Location 📍"),
                "separator": True,
                # "collapsible": True,
                "items": [
                    {
                        "title": _("country"),
                        "icon": "public",
                        "link": reverse_lazy("admin:location_country_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "location.view_country"
                        ),
                    },
                    {
                        "title": _("region"),
                        "icon": "map",
                        "link": reverse_lazy("admin:location_region_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "location.view_region"
                        ),
                    },
                    {
                        "title": _("Address"),
                        "icon": "map",
                        "link": reverse_lazy("admin:location_address_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "location.view_address"
                        ),
                    },
                ],
            },
            {
                "title": _("Application Content 📱"),
                "separator": True,
                "items": [
                    {
                        "title": _("Onboarding"),
                        "icon": "group",
                        "link": reverse_lazy("admin:appInfo_onboarding_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "appInfo.view_onboarding"
                        ),
                    },
                    {
                        "title": _("Banner Group"),
                        "icon": "category",
                        "link": reverse_lazy("admin:appInfo_bannergroup_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "channel.view_bannergroup"
                        ),
                    },
                    {
                        "title": _("Banner"),
                        "icon": "photo",
                        "link": reverse_lazy("admin:appInfo_banner_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "channel.view_banner"
                        ),
                    },
                    {
                        "title": _("PopUp Banner"),
                        "icon": "campaign",
                        "link": reverse_lazy("admin:appInfo_popupbanner_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "channel.view_popupbanner"
                        ),
                    },
                ],
            },
            {
                "title": _("Configuration ⓘ"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Contact Us"),
                        "icon": "call",
                        "link": reverse_lazy("admin:appInfo_contactus_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "appInfo.view_contactus"
                        ),
                    },
                    {
                        "title": _("System Configuration"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:appInfo_systemconfig_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "appInfo.view_systemconfig"
                        ),
                    },
                    {
                        "title": _("Social Accounts"),
                        "icon": "group",
                        "link": reverse_lazy("admin:appInfo_socialaccount_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "appInfo.view_socialaccount"
                        ),
                    },
                    {
                        "title": _("FAQs"),
                        "icon": "help",
                        "link": reverse_lazy("admin:appInfo_faq_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "appInfo.view_faq"
                        ),
                    },
                    {
                        "title": _("App Info"),
                        "icon": "public",
                        "link": reverse_lazy("admin:appInfo_appinfo_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "appInfo.view_appinfo"
                        ),
                    },
                ],
            },
        ],
    },
}


def environment_callback(request):
    if env.environment == "production":
        return ["DEVELOPMENT", "danger"]
    elif env.environment == "staging":
        return ["STAGING", "warning"]
    elif env.environment == "development":
        return ["DEVELOPMENT", "info"]
    elif env.environment == "local":
        return ["LOCAL", "success"]
    else:
        return ["UNKNOWN", "secondary"]


def badge_customers_week_count(request):
    from apps.users.domain.selectors.customer import CustomerSelector

    count = CustomerSelector.last_week_new_customer_count()
    return f"🙋🏻‍♂️: {count}" if count else ""


def get_site_icon(request):
    from apps.users.models.admin import AdminUser

    user = request.user
    if user.is_authenticated and isinstance(user, AdminUser) and user.image:
        return user.image.url
    return static("images/logo.png")
