from abc import ABC
from abc import abstractmethod

from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin as DjangoBaseModelAdmin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget
from unfold.contrib.forms.widgets import WysiwygWidget

from common.mixins.pass_request_to_form import RequestFormMixin


class BaseModelAdminMeta(DjangoBaseModelAdmin.__class__, ABC.__class__):
    pass


class BaseModelAdmin(RequestFormMixin, UnfoldModelAdmin, ABC, metaclass=BaseModelAdminMeta):
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
