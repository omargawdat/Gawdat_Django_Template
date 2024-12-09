from abc import ABC
from abc import abstractmethod

from django.contrib.admin.options import InlineModelAdmin as DjangoInlineModelAdmin
from unfold.admin import StackedInline as UnfoldStackedInline
from unfold.admin import TabularInline as UnfoldTabularInline


class BaseInlineAdminMeta(DjangoInlineModelAdmin.__class__, ABC.__class__):
    pass


class BaseInlineAdmin(ABC, metaclass=BaseInlineAdminMeta):
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @abstractmethod
    def get_fieldsets(self, request, obj=None):
        pass


class StackedInline(UnfoldStackedInline, BaseInlineAdmin):
    pass


class TabularInline(UnfoldTabularInline, BaseInlineAdmin):
    pass
