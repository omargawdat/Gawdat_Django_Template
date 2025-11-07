from django.conf import settings

from ..base import BaseGenerator


class InlineAdminGenerator(BaseGenerator):
    def generate(self, fields: list | None = None) -> None:
        model_name = self.model.__name__
        model_import_path = f"{self.model.__module__}"

        # Get the base admin path from settings
        base_model_admin_path = settings.BASE_MODEL_ADMIN_PATH

        # Import both base classes but use BaseTabularInline by default
        base_imports = (
            f"from {base_model_admin_path} import BaseTabularInline, BaseStackedInline"
        )

        # Import permissions class
        perm_import = f"from .permissions import {model_name}InlinePermissions"

        content = f"""from {model_import_path} import {model_name}
{base_imports}
{perm_import}


class {model_name}Inline({model_name}InlinePermissions, BaseTabularInline):
    model = {model_name}
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()
"""
        self.write_file("inline.py", content)
