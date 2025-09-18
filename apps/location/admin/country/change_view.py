from django.utils.translation import gettext_lazy as _


class CountryChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            _("Country Information"),
            {
                "fields": (
                    "code",
                    "name",
                    "currency",
                    "phone_code",
                    "flag",
                    "is_active",
                )
            },
        ),
        (
            _("Referral Program"),
            {
                "fields": (
                    "app_install_money_inviter",
                    "app_install_money_invitee",
                    "order_money_inviter",
                    "order_money_invitee",
                )
            },
        ),
    )
