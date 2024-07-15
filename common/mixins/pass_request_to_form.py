class RequestFormMixin:
    def get_form(self, request, obj=None, **kwargs):
        FormClass = super().get_form(request, obj, **kwargs)

        class RequestFormClass(FormClass):
            def __new__(cls, *args, **kwargs):
                kwargs["user"] = request.user
                return FormClass(*args, **kwargs)

        return RequestFormClass
