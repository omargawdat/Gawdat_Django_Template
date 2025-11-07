# display_generator.py
from ..base import BaseGenerator


class DisplayGenerator(BaseGenerator):
    def generate(self, fields: list) -> None:
        model_name = self.model.__name__
        model_import_path = f"{self.model.__module__}"
        content = f'''from unfold.decorators import display
from {model_import_path} import {model_name}

class {model_name}DisplayMixin:
    @display(description="{self.model_name_lower}", header=True)
    def display_header(self, {self.model_name_lower}: {model_name}):
        """Display header with image if available."""
        return [
            {self.model_name_lower}.pk,
            "",
            "O",
            {{"path": {self.model_name_lower}.image.url if hasattr({self.model_name_lower}, 'image') and {self.model_name_lower}.image else None}},
        ]
'''
        self.write_file("display.py", content)
