class OnboardingChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        (
            "Main Information",
            {"fields": ("title", "order", "is_active")},
        ),
        (
            "Content",
            {"fields": ("text", "sub_text")},
        ),
        (
            "Media",
            {"fields": ("image",)},
        ),
    )
