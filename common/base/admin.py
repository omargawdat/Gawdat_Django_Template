from abc import ABC
from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.options import ShowFacets
from django.http import HttpRequest
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import StackedInline
from unfold.admin import TabularInline


@dataclass
class FieldPermissions:
    visible: bool | tuple = False
    editable: bool | tuple = False


class DynamicAdminFields(ABC):
    @abstractmethod
    def get_field_rules(self, request, obj=None) -> dict[str, FieldPermissions]:
        """Must be implemented by child classes to define field rules"""

    def get_fieldsets(self, request, obj=None):
        field_rules = self.get_field_rules(request, obj)
        base_fieldsets = super().get_fieldsets(request, obj)

        if not base_fieldsets:
            all_fields = self.get_fields(request, obj)
            visible_fields = [
                field
                for field in all_fields
                if field_rules.get(field, FieldPermissions()).visible
            ]
            return ((None, {"fields": visible_fields}),) if visible_fields else ()

        filtered_fieldsets = []
        for name, options in base_fieldsets:
            if not isinstance(options, dict) or "fields" not in options:
                continue

            visible_fields = [
                field
                for field in options["fields"]
                if field_rules.get(field, FieldPermissions()).visible
            ]

            if visible_fields:
                new_options = options.copy()
                new_options["fields"] = visible_fields
                filtered_fieldsets.append((name, new_options))

        return tuple(filtered_fieldsets)

    def get_readonly_fields(self, request, obj=None):
        field_rules = self.get_field_rules(request, obj)
        base_readonly = super().get_readonly_fields(request, obj)

        readonly_fields = list(base_readonly)
        for field, permissions in field_rules.items():
            if permissions.visible and not permissions.editable:
                readonly_fields.append(field)

        return tuple(readonly_fields)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        field_rules = self.get_field_rules(request, obj)

        for field in list(form.base_fields):
            if not field_rules.get(field, FieldPermissions()).visible:
                del form.base_fields[field]

        return form

    def get_list_display(self, request):
        field_rules = self.get_field_rules(request)
        base_list_display = getattr(self, "list_display", ())
        return tuple(
            field
            for field in base_list_display
            if field not in field_rules or field_rules[field].visible
        )

    def get_list_editable(self, request):
        """
        Filters the ModelAdmin's list_editable fields using the field rules.
        """
        field_rules = self.get_field_rules(request)
        # Retrieve the current list_editable (if defined)
        list_editable = getattr(self, "list_editable", ())
        # Only include fields that are marked editable in our field rules.
        return tuple(
            field
            for field in list_editable
            if field_rules.get(field, FieldPermissions()).editable
        )

    def changelist_view(self, request, extra_context=None):
        """
        Override the changelist view to dynamically update list_editable.
        """
        if hasattr(self, "list_editable"):
            self.list_editable = self.get_list_editable(request)
        return super().changelist_view(request, extra_context=extra_context)


class BaseModelAdminMeta(ModelAdmin.__class__, ABCMeta):
    pass


class BaseModelAdmin(
    DynamicAdminFields,
    SimpleHistoryAdmin,
    UnfoldModelAdmin,
    ABC,
    metaclass=BaseModelAdminMeta,
):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.filter_horizontal = [field.name for field in model._meta.many_to_many]

    empty_value_display = "-"
    compressed_fields = True
    warn_unsaved_form = True
    show_facets = ShowFacets.ALWAYS

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        return super().get_inlines(request, obj)

    @abstractmethod
    def can_add(self, request):
        pass

    @abstractmethod
    def can_change(self, request, obj=None):
        pass

    def has_add_permission(self, request):
        if not super().has_add_permission(request):
            return False
        return self.can_add(request)

    def has_change_permission(self, request, obj=None):
        if not super().has_change_permission(request, obj):
            return False
        return self.can_change(request, obj)

    def has_delete_permission(self, request, obj=None):
        if not super().has_delete_permission(request, obj):
            return False
        return self.can_delete(request, obj)


class BaseInlineMixin(DynamicAdminFields, ABC):
    extra = 1
    show_change_link = True

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)
        if hasattr(self.model, "_meta") and hasattr(self.model._meta, "many_to_many"):
            self.filter_horizontal = [
                field.name for field in self.model._meta.many_to_many
            ]

    @abstractmethod
    def can_add(self, request, obj=None):
        pass

    @abstractmethod
    def can_change(self, request, obj=None):
        pass

    @abstractmethod
    def can_delete(self, request, obj=None):
        pass

    def has_add_permission(self, request, obj=None):
        return self.can_add(request, obj)

    def has_change_permission(self, request, obj=None):
        return self.can_change(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.can_delete(request, obj)


class BaseTabularInlineMeta(TabularInline.__class__, ABCMeta):
    pass


class BaseTabularInline(
    BaseInlineMixin, TabularInline, metaclass=BaseTabularInlineMeta
):
    pass


class BaseStackedInlineMeta(StackedInline.__class__, ABCMeta):
    pass


class BaseStackedInline(
    BaseInlineMixin, StackedInline, metaclass=BaseStackedInlineMeta
):
    pass


class AdminContextLogic:
    """Common context logic for admin views"""

    @staticmethod
    def is_super_admin(request: HttpRequest) -> bool:
        return request.user.is_superuser

    @staticmethod
    def is_normal_admin(request: HttpRequest) -> bool:
        return request.user.is_staff

    @staticmethod
    def is_object_created(obj) -> bool:
        return obj is not None
