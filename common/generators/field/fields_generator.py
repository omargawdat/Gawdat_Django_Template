import re

from ..base import BaseGenerator


class FieldsGenerator(BaseGenerator):
    def generate(self, fields: list) -> None:
        model_name = self.model.__name__
        field_lines = [f'    {field.upper()} = "{field}"' for field in fields]
        content = [
            f"class {model_name}Fields:",
            *field_lines,
            "",
            "    @classmethod",
            "    def get_field_name(cls, model, field):",
            "        return model._meta.get_field(field).name",
        ]

        def update_fields(existing_content):
            """Update existing fields file with any new fields."""
            # Skip if no existing content
            if not existing_content.strip():
                return "\n".join(content)

            # Extract existing fields from the file
            existing_fields = []
            for line in existing_content.split("\n"):
                # Match lines like "    FIELD_NAME = "field_name""
                match = re.match(r'\s+([A-Z_]+)\s+=\s+["\'](.*)["\']', line)
                if match:
                    existing_fields.append(match.group(2))

            # Find fields that need to be added
            new_fields = [field for field in fields if field not in existing_fields]

            # If no new fields, return the existing content
            if not new_fields:
                return existing_content

            # Build updated content by inserting new fields
            lines = existing_content.split("\n")

            # Find the class definition line
            class_line_idx = -1
            for i, line in enumerate(lines):
                if line.startswith(f"class {model_name}Fields:"):
                    class_line_idx = i
                    break

            if class_line_idx == -1:
                # Class definition not found, return new content
                return "\n".join(content)

            # Find where to insert the new fields (before the get_field_name method)
            insert_idx = -1
            for i, line in enumerate(lines[class_line_idx + 1 :], class_line_idx + 1):
                if "@classmethod" in line or "def get_field_name" in line:
                    insert_idx = i
                    break

            if insert_idx == -1:
                # Method not found, append new fields to the end of the class
                # Find the next class or end of file
                for i, line in enumerate(
                    lines[class_line_idx + 1 :], class_line_idx + 1
                ):
                    if line.startswith("class ") or i == len(lines) - 1:
                        insert_idx = i
                        break

            # Insert the new fields
            new_field_lines = [
                f'    {field.upper()} = "{field}"' for field in new_fields
            ]
            updated_lines = lines[:insert_idx] + new_field_lines + lines[insert_idx:]

            return "\n".join(updated_lines)

        # Use update_file instead of write_file to handle existing files
        self.update_file(
            f"{self.model_name_lower}.py", "\n".join(content), update_fields
        )
