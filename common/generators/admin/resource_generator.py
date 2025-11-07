# resource_generator.py
from ..base import BaseGenerator


class ResourceGenerator(BaseGenerator):
    def generate(self, fields: list) -> None:
        model_name = self.model.__name__
        model_import_path = f"{self.model.__module__}"

        content = f"""from import_export import resources

from {model_import_path} import {model_name}


class {model_name}Resource(resources.ModelResource):
    class Meta:
        model = {model_name}
        fields = []
"""
        self.write_file("resource.py", content)
