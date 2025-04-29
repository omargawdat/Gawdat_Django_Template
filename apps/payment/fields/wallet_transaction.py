class WalletTransactionFields:
    WALLET = "wallet"
    TRANSACTION_TYPE = "transaction_type"
    AMOUNT_CURRENCY = "amount_currency"
    AMOUNT = "amount"
    CREATED_AT = "created_at"
    ACTION_BY = "action_by"
    TRANSACTION_NOTE = "transaction_note"
    ATTACHMENT = "attachment"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
