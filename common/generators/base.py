import re
from abc import ABC
from abc import abstractmethod
from pathlib import Path

from .model_utils import ensure_package


class BaseGenerator(ABC):
    """Base class for all code generators."""

    def __init__(
        self, app_name: str, model_name: str, base_path: Path | str, model_class
    ):
        self.base_path = Path(base_path)
        self.model = model_class
        self.model_name_lower = self._to_snake_case(self.model.__name__)

    def _to_snake_case(self, name: str) -> str:
        """Convert CamelCase to snake_case (e.g., TestModelRelated -> test_model_related)"""
        pattern = re.compile(r"(?<!^)(?=[A-Z])")
        return pattern.sub("_", name).lower()

    def write_file(self, filename: str, content: str) -> None:
        """Write content to a file only if the file doesn't already exist."""
        target_dir = self.base_path
        full_path = target_dir / filename

        ensure_package(target_dir)
        if full_path.exists():
            return

        with full_path.open("w") as f:
            f.write(content)

    def update_file(self, filename: str, content: str, update_func=None) -> None:
        """Write content to a file, or update it if it already exists using update_func."""
        target_dir = self.base_path
        full_path = target_dir / filename

        ensure_package(target_dir)

        if full_path.exists():
            if update_func:
                with full_path.open() as f:
                    existing_content = f.read()

                updated_content = update_func(existing_content)

                with full_path.open("w") as f:
                    f.write(updated_content)
        else:
            # File doesn't exist, create it
            with full_path.open("w") as f:
                f.write(content)

    @abstractmethod
    def generate(self, fields: list) -> None:
        """Generate the code files."""
