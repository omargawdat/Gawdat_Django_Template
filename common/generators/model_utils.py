from pathlib import Path

from django.apps import apps


def get_model_fields(app_name: str, model_name: str) -> list:
    """Get direct fields and foreign keys from a model."""
    model = apps.get_model(app_name, model_name)
    return [field.name for field in model._meta.get_fields() if not field.auto_created]


def ensure_package(path: Path | str) -> None:
    """Create directory and __init__.py if they don't exist."""
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    init_file = path_obj / "__init__.py"
    if not init_file.exists():
        with init_file.open("w"):
            pass
