# list_view_generator.py
from ..base import BaseGenerator


class ListViewGenerator(BaseGenerator):
    def generate(self, fields: list) -> None:
        model_name = self.model.__name__
        content = f"""class {model_name}ListView:
    list_display =  ("display_header",)
    list_editable = ()
    list_filter = ()
    date_hierarchy = None
    list_per_page = 50
    list_filter_submit = False
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    search_fields = ()
    search_help_text = ""

    def get_ordering(self, request):
        return ()
"""
        self.write_file("list_view.py", content)
