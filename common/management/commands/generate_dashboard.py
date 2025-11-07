"""Django management command to generate admin dashboard files for models.

This command generates all the boilerplate code needed for a complete admin dashboard
including list views, change views, permissions, display methods, and more.

Usage:
    python manage.py generate_dashboard <app_name> <model_name>

Examples:
    python manage.py generate_dashboard users Customer
    python manage.py generate_dashboard payment Transaction
    python manage.py generate_dashboard location Country --skip-inline

Generated files:
    - admin/<model_name>/list_view.py - List view configuration
    - admin/<model_name>/change_view.py - Change view configuration
    - admin/<model_name>/permissions.py - Permission handling
    - admin/<model_name>/display.py - Display methods
    - admin/<model_name>/resource.py - Export/import configuration
    - admin/<model_name>/inline.py - Inline admin (optional)
    - admin/<model_name>/admin.py - Main admin registration
    - admin/<model_name>/CHECKLIST.md - Configuration review checklist
"""

from pathlib import Path

from django.apps import apps
from django.core.management import BaseCommand

from common.generators.admin.admin_generator import AdminGenerator
from common.generators.admin.change_view_generator import ChangeViewGenerator
from common.generators.admin.checklist_generator import ChecklistGenerator
from common.generators.admin.display_generator import DisplayGenerator
from common.generators.admin.inline import InlineAdminGenerator
from common.generators.admin.list_view_generator import ListViewGenerator
from common.generators.admin.permissions_generator import PermissionsGenerator
from common.generators.admin.resource_generator import ResourceGenerator
from common.generators.model_utils import get_model_fields


class Command(BaseCommand):
    """Generate admin dashboard components for a Django model."""

    help = "Generate admin dashboard files (fields, list view, change view, permissions, etc.) for a model"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="Name of the app (e.g., users)")
        parser.add_argument(
            "model_name", type=str, help="Name of the model (e.g., Customer)"
        )
        parser.add_argument(
            "--skip-inline",
            action="store_true",
            help="Skip generating inline admin",
        )

    def get_app_path(self, app_name: str) -> str:
        """Get absolute path to app directory."""
        try:
            app_config = apps.get_app_config(app_name)
            app_path = Path(app_config.module.__file__).parent
            self.stdout.write(f"Found app path: {app_path}")
        except LookupError as err:
            raise ValueError(f"App '{app_name}' not found in INSTALLED_APPS") from err
        else:
            return str(app_path)

    def handle(self, *args, **options):
        app_name = options["app_name"]
        model_name = options["model_name"]
        skip_inline = options.get("skip_inline", False)

        def _validate_app_path(path: str) -> None:
            if not path:
                raise ValueError("App path cannot be empty")

        try:
            # Get app path
            app_path = self.get_app_path(app_name)
            _validate_app_path(app_path)

            # Get model fields
            fields = get_model_fields(app_name, model_name)
            model_class = apps.get_model(app_name, model_name)

            # Generate admin components
            self._generate_admin_components(
                app_path,
                app_name,
                model_name,
                model_class,
                fields,
                skip_inline=skip_inline,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Successfully generated dashboard files for '{model_name}' model"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"  Location: {app_path}/admin/{model_name.lower()}/"
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
            import traceback

            traceback.print_exc()

    def _generate_admin_components(
        self,
        app_path: str,
        app_name: str,
        model_name: str,
        model_class,
        fields: list,
        *,
        skip_inline: bool,
    ) -> bool:
        """Generate admin dashboard components."""
        base_path = str(Path(app_path) / "admin" / model_name.lower())
        self.stdout.write(f"⏳ Generating admin components in {base_path}")

        # Initialize generators
        generators = [
            (
                "List View",
                ListViewGenerator(app_name, model_name, base_path, model_class),
            ),
            (
                "Change View",
                ChangeViewGenerator(app_name, model_name, base_path, model_class),
            ),
            (
                "Permissions",
                PermissionsGenerator(app_name, model_name, base_path, model_class),
            ),
            ("Display", DisplayGenerator(app_name, model_name, base_path, model_class)),
            (
                "Resource",
                ResourceGenerator(app_name, model_name, base_path, model_class),
            ),
            (
                "Checklist",
                ChecklistGenerator(app_name, model_name, base_path, model_class),
            ),
        ]

        # Add inline generator if not skipped
        has_inline = False
        if not skip_inline:
            generators.insert(
                5,
                (
                    "Inline Admin",
                    InlineAdminGenerator(app_name, model_name, base_path, model_class),
                ),
            )
            has_inline = True

        # Generate all components
        for name, generator in generators:
            if isinstance(generator, InlineAdminGenerator):
                generator.generate(fields=fields)
            else:
                generator.generate(fields)
            self.stdout.write(self.style.SUCCESS(f"  ✓ {name} generated"))

        # Generate main admin registration (needs to know if inline exists)
        admin_generator = AdminGenerator(app_name, model_name, base_path, model_class)
        admin_generator.generate(fields=fields, has_inline=has_inline)
        self.stdout.write(self.style.SUCCESS("  ✓ Admin Registration generated"))

        return has_inline
