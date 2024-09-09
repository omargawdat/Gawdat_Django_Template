from django.templatetags.static import static
from django.urls import reverse_lazy

UNFOLD = {
    "SITE_TITLE": "projectname Admin",
    "SITE_HEADER": "projectname",
    "SHOW_HISTORY": True,
    # "SITE_URL": "",
    "LOGIN": {
        "image": lambda request: static("images/login.png"),
    },
    "SITE_SYMBOL": "anchor",
    # "SITE_ICON": {
    #     "light": lambda request: static("images/identity.png"),
    #     "dark": lambda request: static("images/identity.png"),
    # },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "48x48",
            "type": "image/svg+xml",
            "href": lambda request: static("images/identity.jpg"),
        },
    ],
    "DASHBOARD_CALLBACK": "common.insights.dashboard_callback.dashboard_callback",
    "COLORS": {
        "primary": {
            "50": "235 245 255",
            "100": "207 232 252",
            "200": "174 216 248",
            "300": "140 199 244",
            "400": "100 181 240",
            "500": "60 162 236",
            "600": "30 144 232",
            "700": "20 126 204",
            "800": "15 108 176",
            "900": "10 90 148",
            "950": "5 72 120",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "User Management",
                "separator": True,
                # "collapsible": True,
                "items": [
                    {
                        "title": "Provider",
                        "icon": "surfing",  # Icon for service provider
                        "link": reverse_lazy("admin:users_provider_changelist"),
                        "permission": lambda request: request.user.has_perm("users.view_provider"),
                    },
                    {
                        "title": "Customer",
                        "icon": "person",
                        "link": reverse_lazy("admin:users_customer_changelist"),
                        "permission": lambda request: request.user.has_perm("users.view_staffuser"),
                    },
                    {
                        "title": "Staff",
                        "icon": "frame_person",
                        "link": reverse_lazy("admin:users_staffuser_changelist"),
                        "permission": lambda request: request.user.has_perm("users.view_staffuser"),
                    },
                    {
                        "title": "Groups",
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.has_perm("users.view_staffuser"),
                    },
                ],
            },
            {
                "title": "App Info",
                "separator": True,
                # "collapsible": True,
                "items": [
                    {
                        "title": "Social Account",
                        "icon": "group",  # Represents social or group of people
                        "link": reverse_lazy("admin:appInfo_socialaccount_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "appInfo.view_socialaccount"
                        ),
                    },
                    {
                        "title": "About Us",
                        "icon": "info",  # Represents information
                        "link": reverse_lazy("admin:appInfo_aboutus_changelist"),
                        "permission": lambda request: request.user.has_perm("appInfo.view_aboutus"),
                    },
                    {
                        "title": "Terms and Conditions",
                        "icon": "gavel",  # Represents legal or terms
                        "link": reverse_lazy("admin:appInfo_termsandconditions_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "appInfo.view_termsandconditions"
                        ),
                    },
                ],
            },
        ],
    },
    "TABS": [],
}

# {
#     "title": "Navigation",
#     "separator": True,
#     # "collapsible": True,
#     "items": [
#         {
#             "title": "Dashboard",
#             "icon": "dashboard",
#             "link": reverse_lazy("admin:index"),
#         },
#     ],
# },

# {
#     "title": "Notification",
#     "separator": True,
#     # "collapsible": True,
#     "items": [
#         {
#             "title": "Notification",
#             "icon": "notifications",
#             "link": reverse_lazy("admin:notification_notification_changelist"),
#             "permission": lambda request: request.user.has_perm(
#                 "notification.view_notification"
#             ),
#         },
#     ],
# },
