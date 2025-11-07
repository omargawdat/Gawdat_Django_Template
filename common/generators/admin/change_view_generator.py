# change_view_generator.py
from ..base import BaseGenerator


class ChangeViewGenerator(BaseGenerator):
    def generate(self, fields: list) -> None:
        model_name = self.model.__name__
        content = f"""class {model_name}ChangeView:
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = ()
    fieldsets = (
        ("Information", {{"fields": ()}}),
    )
    inlines = []
"""
        self.write_file("change_view.py", content)
