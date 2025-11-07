# context_generator.py

from ..base import BaseGenerator


class ContextGenerator(BaseGenerator):
    def generate(self, fields: list[str] | None = None) -> None:
        model_name = self.model.__name__
        content = f"""from typing import Optional
from django.http import HttpRequest
from {self.model.__module__} import {model_name}
"""
        self.write_file("context.py", content)
