class PaymentFields:
    CUSTOMER = "customer"
    PRICE_BEFORE_DISCOUNT_CURRENCY = "price_before_discount_currency"
    PRICE_BEFORE_DISCOUNT = "price_before_discount"
    PRICE_AFTER_DISCOUNT_CURRENCY = "price_after_discount_currency"
    PRICE_AFTER_DISCOUNT = "price_after_discount"
    PAYMENT_TYPE = "payment_type"
    IS_PAID = "is_paid"
    PAYMENT_CHARGE_ID = "payment_charge_id"
    BANK_TRANSACTION_RESPONSE = "bank_transaction_response"
    CREATED_AT = "created_at"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
