class WalletTransactionChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        ("Basic Information", {"fields": ("wallet", "transaction_type")}),
        ("Financial Details", {"fields": ("amount",)}),
        ("Additional Information", {"fields": ("transaction_note", "attachment")}),
    )
