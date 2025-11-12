from django.conf import settings

from ..base import BaseGenerator


class AdminGenerator(BaseGenerator):
    def generate(self, fields: list, *, has_inline: bool = False) -> None:
        """
        Generate admin class for a model.

        Args:
            fields: List of fields to include in the admin
            has_inline: Whether to include inline import (keyword-only)
        """
        model_name = self.model.__name__
        model_import_path = f"{self.model.__module__}"
        base_model_admin_path = settings.BASE_MODEL_ADMIN_PATH

        content = f"""from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import XLSX
from unfold.contrib.import_export.forms import ExportForm
from .list_view import {model_name}ListView
from .change_view import {model_name}ChangeView
from .permissions import {model_name}AdminPermissions
from .display import {model_name}DisplayMixin
from .resource import {model_name}Resource
from {model_import_path} import {model_name}
from {base_model_admin_path} import BaseModelAdmin

@admin.register({model_name})
class {model_name}Admin(
    {model_name}DisplayMixin,
    {model_name}ListView,
    {model_name}ChangeView,
    {model_name}AdminPermissions,
    BaseModelAdmin,
):
    resource_class = {model_name}Resource
    export_form_class = ExportForm
    formats = [XLSX]
"""
        self.write_file("admin.py", content)
