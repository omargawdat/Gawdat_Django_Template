from django.urls import reverse_lazy

UNFOLD = {
    "SITE_TITLE": "template_app",
    "SITE_HEADER": "template_app",
    "SHOW_HISTORY": True,
    # "SHOW_VIEW_ON_SITE": True,
    # "SITE_URL": "",
    # "LOGIN": {
    #     "image": lambda request: static("images/login.png"),
    # },
    # "SITE_ICON": {
    #     "light": lambda request: static("images/identity.svg"),
    #     "dark": lambda request: static("images/identity.svg"),
    # },
    # "SITE_FAVICONS": [
    #     {
    #         "rel": "icon",
    #         "sizes": "48x48",
    #         "type": "image/svg+xml",
    #         "href": lambda request: static("images/identity.svg"),
    #     },
    # ],
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
                "title": "Navigation",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "User Management",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Staff",
                        "icon": "person",
                        "link": reverse_lazy("admin:users_staffuser_changelist"),
                    },
                    {
                        "title": "Groups",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [],
}
