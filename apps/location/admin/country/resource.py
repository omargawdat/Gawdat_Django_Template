from import_export import resources

from apps.location.models.country import Country


class CountryResource(resources.ModelResource):
    class Meta:
        model = Country
        fields = [
            "code",
            "is_active",
            "app_install_money_inviter",
            "app_install_money_invitee",
            "order_money_inviter",
            "order_money_invitee",
        ]
