from django.contrib.auth.hashers import make_password


class HashPasswordMixin:
    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:
            password = form.cleaned_data.get("password")
            if password:
                obj.password = make_password(password)
        super().save_model(request, obj, form, change)  # type: ignore
