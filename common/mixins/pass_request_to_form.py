class RequestFormMixin:
    def get_form(self, request, obj=None, **kwargs):
        FormClass = super().get_form(request, obj, **kwargs)
        readonly_fields = self.get_readonly_fields(request, obj)

        class RequestFormClass(FormClass):
            def __init__(self, *args, **kwargs):
                user = kwargs.pop("request", request).user
                readonly_data = self.get_readonly_data(obj, readonly_fields)
                kwargs.update(user=user, readonly_fields=readonly_data)
                super().__init__(*args, **kwargs)

        RequestFormClass.get_readonly_data = staticmethod(self.get_readonly_data)
        return RequestFormClass

    def get_readonly_fields(self, request, obj=None):
        return getattr(self, "readonly_fields", ())

    @staticmethod
    def get_readonly_data(obj, fields):
        if not obj:
            return {}
        return {field: getattr(obj, field) for field in fields}
