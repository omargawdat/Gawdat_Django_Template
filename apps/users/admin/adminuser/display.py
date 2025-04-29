from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from apps.users.models.admin import AdminUser


class AdminUserDisplayMixin:
    @display(description=_("Admin"), header=True)
    def display_header(self, admin_user: AdminUser):
        return [
            admin_user,
            _("ID: %s") % admin_user.pk,
            "🧑‍💼",
            {
                "path": admin_user.image.url if admin_user.image else None,
                "squared": False,
                "borderless": True,
            },
        ]

    @display(label={"True": "success", "False": "danger"}, description=_("Is Active"))
    def display_is_active_driver(self, admin: AdminUser) -> str:
        return "True" if admin.is_active else "False"

    @display(description=_("Date joined ago"), label="info")
    def display_date_joined_time(self, admin: AdminUser):
        return f"{timesince(admin.date_joined, timezone.now())}"
