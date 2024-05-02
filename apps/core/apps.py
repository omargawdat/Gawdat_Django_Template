import importlib
import os

from django.apps import AppConfig, apps


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        # import admins
        for app_config in apps.get_app_configs():
            self.import_modules_from_directory(app_config.path, "admin", app_config.name)

        # import signals
        self.import_modules_from_directory(self.path, "signals", self.name)

        # Import models
        for app_config in apps.get_app_configs():
            self.import_modules_from_directory(app_config.path, "models", app_config.name)

    def import_modules_from_directory(self, base_path, subdirectory, app_name):
        directory_path = os.path.join(base_path, subdirectory)
        if os.path.exists(directory_path):
            modules = [f[:-3] for f in os.listdir(directory_path) if f.endswith(".py") and not f.startswith("__")]
            for module in modules:
                importlib.import_module(f"{app_name}.{subdirectory}.{module}")
