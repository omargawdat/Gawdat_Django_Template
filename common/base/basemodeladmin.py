from abc import ABC
from abc import ABCMeta
from abc import abstractmethod

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from rest_framework.exceptions import APIException
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget
from unfold.contrib.forms.widgets import WysiwygWidget

from common.mixins.pass_request_to_form import RequestFormMixin  # type: ignore


class BaseModelAdminMeta(ModelAdmin.__class__, ABCMeta):
    pass


class BaseModelAdmin(
    RequestFormMixin,
    UnfoldModelAdmin,
    ABC,
    metaclass=BaseModelAdminMeta,
):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.filter_horizontal = [
            field.name
            for field in model._meta.many_to_many  # noqa: SLF001
        ]  # SLF001

    empty_value_display = "-"
    show_facets = admin.ShowFacets.ALWAYS
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }
    compressed_fields = True
    warn_unsaved_form = True

    def get_form(self, request, obj=None, **kwargs):
        form_class = super().get_form(request, obj, **kwargs)  # N806 fixed

        # Explicitly ignore SLF001 for accessing protected members
        original_post_clean = form_class.clean

        def handle_api_exception(form_instance, api_error):
            if hasattr(api_error.detail, "items"):
                errors = {}
                for field, error in api_error.detail.items():
                    if field in form_instance.fields:
                        form_instance.add_error(field, error)
                    else:
                        errors[field] = error
                if errors:
                    form_instance.add_error(None, errors)
            else:
                form_instance.add_error(None, str(api_error.detail))

        def clean(form_instance):  # Renamed from _post_clean
            try:
                original_post_clean(form_instance)
            except APIException as api_error:
                try:
                    handle_api_exception(form_instance, api_error)
                except (ValueError, AttributeError, KeyError):  # BLE001 fixed
                    form_instance.add_error(None, str(api_error.detail))

        form_class.clean = clean
        return form_class

    @property
    @abstractmethod
    def form(self):
        pass

    @abstractmethod
    def get_readonly_fields(self, request, obj=None):
        pass

    @abstractmethod
    def get_fieldsets(self, request, obj=None):
        pass

    @abstractmethod
    def has_add_permission(self, request):
        pass

    @abstractmethod
    def has_change_permission(self, request, obj=None):
        pass

    @abstractmethod
    def has_delete_permission(self, request, obj=None):
        pass
