import importlib
import os

from django.apps import AppConfig, apps


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        for app_config in apps.get_app_configs():
            admin_path = os.path.join(app_config.path, 'admin')
            if os.path.exists(admin_path):
                admin_modules = [f[:-3] for f in os.listdir(admin_path) if f.endswith('.py') and not f.startswith('__')]
                for module in admin_modules:
                    importlib.import_module(f"{app_config.name}.admin.{module}")
