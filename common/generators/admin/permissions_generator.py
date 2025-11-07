# permissions_generator.py
import re
from importlib import import_module

from django.conf import settings

from ..base import BaseGenerator

# Import dynamically from the path in settings
base_model_admin_path = settings.BASE_MODEL_ADMIN_PATH
admin_module = import_module(base_model_admin_path)
AdminContextLogic = admin_module.AdminContextLogic


class PermissionsGenerator(BaseGenerator):
    def generate(self, fields: list[str]) -> None:  # noqa: PLR0915
        """Generate permissions file - complex due to comprehensive permission handling."""
        model_name = self.model.__name__
        field_rules = [
            f'            "{field}": FieldPermissions(\n'
            "                visible=(\n"
            "                    normal_admin\n"
            "                ),\n"
            "                editable=(\n"
            "                ),\n"
            "            )"
            for field in fields
        ]

        # Pre-join the field rules to avoid backslash in f-string expression
        joined_field_rules = ",\n".join(field_rules)

        imports = f"""from typing import Optional, Dict
from django.http import HttpRequest
from {base_model_admin_path} import FieldPermissions, AdminContextLogic
from {self.model.__module__} import {model_name}
"""

        base_class = f"""
class Base{model_name}Permissions:
    def get_field_rules(self, request: HttpRequest, {self.model_name_lower}: Optional[{model_name}] = None) -> Dict:
        super_admin = AdminContextLogic.is_super_admin(request)
        normal_admin = AdminContextLogic.is_normal_admin(request)
        created = AdminContextLogic.is_object_created({self.model_name_lower})

        return {{
{joined_field_rules}
        }}
        """

        admin_class = f"""
class {model_name}AdminPermissions(Base{model_name}Permissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
"""

        inline_class = f"""
class {model_name}InlinePermissions(Base{model_name}Permissions):
    def can_add(self, request, obj=None):
        return False

    def can_change(self, request, obj=None):
        return False

    def can_delete(self, request, obj=None):
        return False
"""

        content = imports + base_class + admin_class + inline_class

        def update_permissions(existing_content):  # noqa: PLR0912
            """Update existing permissions file with any new fields."""
            # Skip if no existing content
            if not existing_content.strip():
                return content

            # Check if file has the new structure with Base, Admin and Inline classes
            base_pattern = f"class Base{model_name}Permissions"
            admin_pattern = f"class {model_name}AdminPermissions"
            inline_pattern = f"class {model_name}InlinePermissions"

            has_new_structure = (
                base_pattern in existing_content
                and admin_pattern in existing_content
                and inline_pattern in existing_content
            )

            # If doesn't have new structure, regenerate
            if not has_new_structure:
                return content

            # Extract existing fields from the file (looking for "field_name": FieldPermissions pattern)
            existing_fields = []
            field_pattern = r'"([a-z_]+)"\s*:\s*FieldPermissions'
            for line in existing_content.split("\n"):
                match = re.search(field_pattern, line)
                if match:
                    existing_fields.append(match.group(1))

            # Find fields that need to be added
            new_fields = [field for field in fields if field not in existing_fields]

            # If no new fields, return the existing content
            if not new_fields:
                return existing_content

            # Generate rules for new fields
            new_field_rules = []
            for i, field in enumerate(new_fields):
                rule = f'            "{field}": FieldPermissions(\n'
                rule += "                visible=(\n"
                rule += "                    normal_admin\n"
                rule += "                ),\n"
                rule += "                editable=(\n"
                rule += "                ),\n"
                rule += "            )"

                # Add a comma if this isn't the last field
                if i < len(new_fields) - 1:
                    rule += ","

                new_field_rules.append(rule)

            # Find where to insert the new fields
            lines = existing_content.split("\n")

            # Look for the return statement and the closing brace
            return_idx = -1
            closing_brace_idx = -1

            for i, line in enumerate(lines):
                if "return {" in line:
                    return_idx = i
                    break

            if return_idx == -1:
                # Can't find where to insert, return new content
                return content

            # Find closing brace after return
            for i, line in enumerate(lines[return_idx:], return_idx):
                if (
                    "}" in line and '"' not in line and "'" not in line
                ):  # Avoid matching braces in strings
                    closing_brace_idx = i
                    break

            if closing_brace_idx == -1:
                # Can't find closing brace, return new content
                return content

            # Add a comma to the last existing field if needed
            for i in range(closing_brace_idx - 1, return_idx, -1):
                line = lines[i].strip()
                if line and not line.endswith(",") and not line.startswith("#"):
                    lines[i] = lines[i] + ","
                    break
                if line and line.endswith((",", "{")):
                    # Already has a comma or is the opening brace
                    break

            # Insert new fields before the closing brace
            new_content = (
                lines[:closing_brace_idx] + new_field_rules + lines[closing_brace_idx:]
            )

            return "\n".join(new_content)

        # Use update_file instead of write_file to handle existing files
        self.update_file("permissions.py", content, update_permissions)
