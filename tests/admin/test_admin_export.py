"""
Test admin export functionality
"""

import pytest
from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export.admin import ImportExportModelAdmin

MIN_CSV_LINES = 2  # Header + at least one data row
MIN_HEADER_LENGTH = 10  # Minimum length for a valid header


@pytest.mark.django_db
class TestAdminExport:
    """Test CSV export functionality for admin models"""

    def test_csv_export_not_empty(self):
        """Test CSV export returns non-empty data for all configured models"""
        for model, model_admin in admin.site._registry.items():
            # Skip models without export configured
            if (
                not hasattr(model_admin, "resource_class")
                or model_admin.resource_class is None
            ):
                continue

            # Skip models that don't have export functionality
            # Check for ExportActionModelAdmin or ImportExportModelAdmin mixins
            if not isinstance(
                model_admin, (ExportActionModelAdmin, ImportExportModelAdmin)
            ):
                continue

            # Skip if no data exists for this model
            if not hasattr(model, "objects") or model.objects.count() == 0:
                continue

            app_label = model._meta.app_label
            model_name = model._meta.model_name

            # Get the resource class and export data
            resource_class = model_admin.resource_class
            resource = resource_class()

            try:
                # Export data using the resource
                dataset = resource.export()

                # Get CSV content
                csv_content = dataset.csv

                # Check CSV is not empty
                assert len(csv_content) > 0, (
                    f"Export for {app_label}.{model_name} returned empty CSV"
                )

                # Check CSV has actual content (not just whitespace/newlines)
                csv_stripped = csv_content.strip()
                assert len(csv_stripped) > 0, (
                    f"Export for {app_label}.{model_name} contains only whitespace/newlines. "
                    f"This usually means fields=[] in the Resource class."
                )

                # Check CSV has actual lines with content
                lines = [
                    line.strip() for line in csv_content.split("\n") if line.strip()
                ]
                assert len(lines) > 0, (
                    f"Export for {app_label}.{model_name} has no content lines. "
                    f"This usually means fields=[] in the Resource class."
                )

                # Check CSV has data rows (header + at least one data row)
                assert len(lines) >= MIN_CSV_LINES, (
                    f"Export for {app_label}.{model_name} has only {len(lines)} line(s). "
                    f"Expected header + data rows. Check Resource class fields configuration."
                )

                # Check header row has actual columns
                header = lines[0]
                assert "," in header or len(header) > MIN_HEADER_LENGTH, (
                    f"Export for {app_label}.{model_name} has suspicious header: '{header}'. "
                    f"CSV should have multiple columns (commas). "
                    f"Check if fields are properly defined in Resource class."
                )

            except Exception as e:
                pytest.fail(f"Export test failed for {app_label}.{model_name}: {e}")
