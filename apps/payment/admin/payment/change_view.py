from apps.payment.fields.payment import PaymentFields


class PaymentChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    PaymentFields.CUSTOMER,
                    PaymentFields.PRICE_BEFORE_DISCOUNT,
                    PaymentFields.PRICE_BEFORE_DISCOUNT_CURRENCY,
                    PaymentFields.PRICE_AFTER_DISCOUNT,
                    PaymentFields.PRICE_AFTER_DISCOUNT_CURRENCY,
                    PaymentFields.PAYMENT_TYPE,
                )
            },
        ),
        (
            "Status & Metadata",
            {
                "fields": (
                    PaymentFields.IS_PAID,
                    PaymentFields.PAYMENT_CHARGE_ID,
                    PaymentFields.BANK_TRANSACTION_RESPONSE,
                    PaymentFields.CREATED_AT,
                )
            },
        ),
    )
    inlines = []
