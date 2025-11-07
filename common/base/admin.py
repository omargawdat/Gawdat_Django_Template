from abc import ABC
from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.options import ShowFacets
from django.http import HttpRequest
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import StackedInline
from unfold.admin import TabularInline

from config.helpers.env import env


@dataclass
class FieldPermissions:
    visible: bool | tuple = False
    editable: bool | tuple = False

    def is_visible(self) -> bool:
        if isinstance(self.visible, bool):
            return self.visible
        return any(self.visible) if self.visible else False

    def is_editable(self) -> bool:
        if isinstance(self.editable, bool):
            return self.editable
        return any(self.editable) if self.editable else False


class DynamicAdminFields(ABC):
    """
    Mixin for dynamic field-level permissions in Django admin.

    Uses Django's field resolution chain for cleaner implementation.
    Override get_field_config() to define your field rules.
    """

    @abstractmethod
    def get_field_config(
        self, request: HttpRequest, obj: Any | None = None
    ) -> dict[str, FieldPermissions]:
        """
        Define field configuration rules.

        Returns:
            Dict mapping field names to FieldPermissions objects.
            Only include fields that need special handling.

        Example:
            def get_field_config(self, request, obj=None):
                ctx = AdminContext(request, obj)
                return {
                    'email': FieldPermissions(visible=True, editable=False),
                    'balance': FieldPermissions(
                        visible=(ctx.is_staff,),
                        editable=(ctx.is_super_admin,),
                    ),
                }
        """

    def get_fields(self, request: HttpRequest, obj: Any | None = None) -> list[str]:
        """
        Override Django's get_fields() to filter visible fields.

        This is used when no fieldsets are defined.
        """
        field_config = self.get_field_config(request, obj)
        all_fields = super().get_fields(request, obj)

        return [
            field
            for field in all_fields
            if field_config.get(field, FieldPermissions()).is_visible()
        ]

    def get_fieldsets(
        self, request: HttpRequest, obj: Any | None = None
    ) -> tuple[tuple[str | None, dict], ...]:
        """
        Override to filter fieldsets when they are explicitly defined.

        This handles cases where admin classes have hardcoded fieldsets.
        """
        field_config = self.get_field_config(request, obj)
        base_fieldsets = super().get_fieldsets(request, obj)

        if not base_fieldsets:
            # No fieldsets defined, Django will use get_fields() instead
            return base_fieldsets

        # Filter existing fieldsets
        filtered_fieldsets = []
        for name, options in base_fieldsets:
            if not isinstance(options, dict) or "fields" not in options:
                filtered_fieldsets.append((name, options))
                continue

            visible_fields = [
                field
                for field in options["fields"]
                if field_config.get(field, FieldPermissions()).is_visible()
            ]

            if visible_fields:
                new_options = options.copy()
                new_options["fields"] = visible_fields
                filtered_fieldsets.append((name, new_options))

        return tuple(filtered_fieldsets)

    def get_readonly_fields(
        self, request: HttpRequest, obj: Any | None = None
    ) -> tuple[str, ...]:
        """Get readonly fields based on field config."""
        field_config = self.get_field_config(request, obj)
        base_readonly = super().get_readonly_fields(request, obj)

        readonly_fields = set(base_readonly)
        for field, permissions in field_config.items():
            if permissions.is_visible() and not permissions.is_editable():
                readonly_fields.add(field)

        return tuple(readonly_fields)

    def get_list_display(self, request: HttpRequest) -> tuple[str, ...]:
        """Filter list display columns by visibility (optional override)."""
        field_config = self.get_field_config(request)
        base_list_display = getattr(self, "list_display", ())
        return tuple(
            field
            for field in base_list_display
            if field_config.get(field, FieldPermissions()).is_visible()
        )

    def get_list_editable(self, request: HttpRequest) -> tuple[str, ...]:
        """Filter list editable fields by editability (optional override)."""
        field_config = self.get_field_config(request)
        list_editable = getattr(self, "list_editable", ())
        return tuple(
            field
            for field in list_editable
            if field_config.get(field, FieldPermissions()).is_editable()
        )


class BaseModelAdminMeta(ModelAdmin.__class__, ABCMeta):
    pass


class BaseModelAdmin(
    DynamicAdminFields,
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
    change_form_show_cancel_button = True
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

    @abstractmethod
    def can_delete(self, request, obj=None):
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


@dataclass
class AdminContext:
    """
    Unified context for admin views.

    Provides convenient properties for common permission checks and context logic.

    Example:
        context = AdminContext(request, obj)
        if context.is_super_admin and context.is_created:
            # Allow editing
    """

    request: HttpRequest
    obj: Any | None = None

    @property
    def is_super_admin(self) -> bool:
        """Check if user is a superuser."""
        return self.request.user.is_superuser

    @property
    def is_staff(self) -> bool:
        """Check if user has staff status."""
        return self.request.user.is_staff

    @property
    def is_created(self) -> bool:
        """Check if object exists (edit view)."""
        return self.obj is not None

    @property
    def is_creating(self) -> bool:
        """Check if creating new object (add view)."""
        return self.obj is None

    @property
    def is_non_production(self) -> bool:
        """Check if running in non-production environment."""
        return env.environment in ["development", "local"]

    # Backward compatibility aliases
    @staticmethod
    def is_super_admin_static(request: HttpRequest) -> bool:
        """Deprecated: Use AdminContext(request).is_super_admin instead."""
        return request.user.is_superuser

    @staticmethod
    def is_normal_admin(request: HttpRequest) -> bool:
        """Deprecated: Use AdminContext(request).is_staff instead."""
        return request.user.is_staff

    @staticmethod
    def is_object_created(obj: Any) -> bool:
        """Deprecated: Use AdminContext(request, obj).is_created instead."""
        return obj is not None

    @staticmethod
    def is_non_production_env() -> bool:
        """Deprecated: Use AdminContext(request).is_non_production instead."""
        return env.environment in ["development", "local"]


# Backward compatibility: Keep old name as alias
AdminContextLogic = AdminContext
