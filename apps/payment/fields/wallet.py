class WalletFields:
    USER = "user"
    BALANCE_CURRENCY = "balance_currency"
    BALANCE = "balance"
    IS_USE_WALLET_IN_PAYMENT = "is_use_wallet_in_payment"
    LAST_UPDATE = "last_update"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
