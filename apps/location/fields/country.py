class CountryFields:
    CODE = "code"
    CURRENCY = "currency"
    NAME = "name"
    NAME_AR = "name_ar"
    NAME_EN = "name_en"
    PHONE_CODE = "phone_code"
    FLAG = "flag"
    IS_ACTIVE = "is_active"
    APP_INSTALL_MONEY_INVITER = "app_install_money_inviter"
    APP_INSTALL_MONEY_INVITEE = "app_install_money_invitee"
    ORDER_MONEY_INVITER = "order_money_inviter"
    ORDER_MONEY_INVITEE = "order_money_invitee"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
