class WalletChangeView:
    filter_horizontal = ()
    compressed_fields = False
    autocomplete_fields = ()
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "user",
                    "balance",
                    "balance_currency",
                    "is_use_wallet_in_payment",
                )
            },
        ),
    )
