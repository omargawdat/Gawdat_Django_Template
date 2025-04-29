from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from config.helpers.env import env

UNFOLD = {
    "SITE_TITLE": "projectname Admin Prod",
    "SITE_HEADER": "projectname",
    "SHOW_HISTORY": True,
    "SHOW_LANGUAGES": True,
    "SHOW_BACK_BUTTON": True,
    "SITE_URL": "https://www.google.com/",  # todo: set this to the actual site url
    "LOGIN": {
        "image": lambda request: static("images/login.png"),
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
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-600)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
            "important-dark": "var(--color-base-100)",
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
                        "permissions": lambda request: request.user.has_perm(
                            "users.view_customer"
                        ),
                    },
                ],
            },
            {
                "title": _("Products 🛍️"),
                "separator": True,
                "items": [
                    {
                        "title": _("Product"),
                        "icon": "inventory",
                        "link": reverse_lazy("admin:products_product_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "products.view_product"
                        ),
                    },
                    {
                        "title": _("Category"),
                        "icon": "category",
                        "link": reverse_lazy("admin:products_category_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "products.view_category"
                        ),
                    },
                    {
                        "title": _("Brand"),
                        "icon": "branding_watermark",
                        "link": reverse_lazy("admin:products_brand_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "products.view_brand"
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
                        "permissions": lambda request: request.user.has_perm(
                            "payment.view_wallet"
                        ),
                    },
                    {
                        "title": _("Wallet Transaction"),
                        "icon": "account_balance_wallet",
                        "link": reverse_lazy(
                            "admin:payment_wallettransaction_changelist"
                        ),
                        "permissions": lambda request: request.user.has_perm(
                            "payment.view_wallettransaction"
                        ),
                    },
                ],
            },
            {
                "title": _("Notification 📢"),
                "separator": True,
                "items": [
                    {
                        "title": _("Notification"),
                        "icon": "notifications",
                        "link": reverse_lazy("admin:channel_notification_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "channel.view_notification"
                        ),
                    },
                ],
            },
            {
                "title": _("Location 📍"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("country"),
                        "icon": "public",
                        "link": reverse_lazy("admin:location_country_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "location.view_country"
                        ),
                    },
                    {
                        "title": _("region"),
                        "icon": "map",
                        "link": reverse_lazy("admin:location_region_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "location.view_region"
                        ),
                    },
                ],
            },
            {
                "title": _("Admin & Group 👥"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Admin"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_adminuser_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "users.view_adminuser"
                        ),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "auth.view_group"
                        ),
                    },
                ],
            },
            {
                "title": _("App Info ⓘ"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("App Info"),
                        "icon": "public",
                        "link": reverse_lazy("admin:appInfo_appinfo_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "appInfo.view_appinfo"
                        ),
                    },
                    {
                        "title": _("FAQs"),
                        "icon": "help",
                        "link": reverse_lazy("admin:appInfo_faq_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "appInfo.view_faq"
                        ),
                    },
                    {
                        "title": _("System Configuration"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:appInfo_systemconfig_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "appInfo.view_systemconfig"
                        ),
                    },
                    {
                        "title": _("Social Accounts"),
                        "icon": "group",
                        "link": reverse_lazy("admin:appInfo_socialaccount_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "appInfo.view_socialaccount"
                        ),
                    },
                    {
                        "title": _("Banner"),
                        "icon": "image",
                        "link": reverse_lazy("admin:products_banner_changelist"),
                        "permissions": lambda request: request.user.has_perm(
                            "products.view_banner"
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
    return static("images/identity.png")
