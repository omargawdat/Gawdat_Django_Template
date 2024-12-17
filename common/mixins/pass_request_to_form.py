# type: ignore
# ruff: noqa
class RequestFormMixin:
    def get_form(self, request, obj=None, **kwargs):
        FormClass = super().get_form(request, obj, **kwargs)

        if hasattr(self, "get_readonly_fields"):
            readonly_fields = self.get_readonly_fields(request, obj)
        else:
            readonly_fields = getattr(self, "readonly_fields", ())

        class RequestFormClass(FormClass):
            def __init__(self, *args, **kwargs):
                self.request = kwargs.pop("request", request)
                self.user = self.request.user
                self.readonly_data = self.get_readonly_data(obj, readonly_fields)
                super().__init__(*args, **kwargs)

            def __getattribute__(self, name):
                if name == "cleaned_data":
                    data = super().__getattribute__("cleaned_data")
                    readonly_data = super().__getattribute__("readonly_data")
                    data.update(readonly_data)
                    return data
                return super().__getattribute__(name)

            def clean(self):
                cleaned_data = super().clean()
                for field, value in self.readonly_data.items():
                    cleaned_data[field] = value
                return cleaned_data

            @staticmethod
            def get_readonly_data(obj, fields):
                if not obj:
                    return {}
                return {
                    field: getattr(obj, field)
                    for field in fields
                    if hasattr(obj, field)
                }

        return RequestFormClass
