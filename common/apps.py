import importlib
import os
from pathlib import Path

from django.apps import AppConfig
from django.apps import apps


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "common"

    def ready(self):
        import common.money_patches  # noqa

        # this code is for importing admins
        for app_config in apps.get_app_configs():
            admin_dir = Path(app_config.path) / "admin"
            if admin_dir.is_dir():
                # Import all .py files in the admin directory
                for file in admin_dir.glob("*.py"):
                    if file.name != "__init__.py":
                        module_name = f"{app_config.name}.admin.{file.stem}"
                        importlib.import_module(module_name)

                # Import all .py files from subdirectories
                for subdir in admin_dir.iterdir():
                    if subdir.is_dir():
                        for file in subdir.glob("*.py"):
                            if file.name != "__init__.py":
                                module_name = (
                                    f"{app_config.name}.admin.{subdir.name}.{file.stem}"
                                )
                                importlib.import_module(module_name)

        # Import models
        for app_config in apps.get_app_configs():
            self.import_modules_from_directory(
                app_config.path,
                "models",
                app_config.name,
            )

    def import_modules_from_directory(self, base_path, subdirectory, app_name):
        directory_path = Path(base_path) / subdirectory
        if Path(directory_path).exists():
            modules = [
                f[:-3]
                for f in os.listdir(directory_path)
                if f.endswith(".py") and not f.startswith("__")
            ]
            for module in modules:
                importlib.import_module(f"{app_name}.{subdirectory}.{module}")
