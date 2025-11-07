class PaymentChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "customer",
                    "price_before_discount",
                    "price_before_discount_currency",
                    "price_after_discount",
                    "price_after_discount_currency",
                    "payment_type",
                )
            },
        ),
        (
            "Status & Metadata",
            {
                "fields": (
                    "is_paid",
                    "payment_charge_id",
                    "bank_transaction_response",
                    "created_at",
                )
            },
        ),
    )
    inlines = []
