class RequestFormMixin:
    def get_form(self, request, obj=None, **kwargs):
        FormClass = super().get_form(request, obj, **kwargs)
        readonly_fields = getattr(self, "readonly_fields", ())

        class RequestFormClass(FormClass):
            def __init__(self, *args, **kwargs):
                kwargs["user"] = request.user
                kwargs["readonly_fields"] = readonly_fields
                super().__init__(*args, **kwargs)

        return RequestFormClass
