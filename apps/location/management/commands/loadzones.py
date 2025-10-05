import json
import re
from pathlib import Path

from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand
from django.db import DataError
from django.db import IntegrityError
from django.db import OperationalError

from apps.location.models.country import Country
from apps.location.models.region import Region


class Command(BaseCommand):
    help = "Imports Zone data from GeoJSON files in nested directories."

    def __init__(self):
        super().__init__()
        self.total_created = 0
        self.total_updated = 0
        self.total_failed = 0

    def handle(self, *args, **options):
        base_dir = Path("assets/countries/working")

        if not base_dir.exists():
            self.stdout.write(
                self.style.ERROR(f"Base directory does not exist: {base_dir}")
            )
            return

        self.stdout.write(self.style.SUCCESS(f"Base directory: {base_dir}"))

        # Process files in the base directory
        base_geojson_files = self.get_geojson_files(base_dir)
        self.stdout.write(
            self.style.SUCCESS(
                f"Processing {len(base_geojson_files)} files in base directory."
            )
        )
        for file_path in base_geojson_files:
            self.process_file(file_path)

        # Process nested directories
        country_dirs = self.get_directories(base_dir)
        self.stdout.write(
            self.style.SUCCESS(f"Processing {len(country_dirs)} nested directories.")
        )
        for country_path in country_dirs:
            self.stdout.write(
                self.style.SUCCESS(f"Processing directory: {country_path}")
            )
            geojson_files = self.get_geojson_files(country_path)
            for file_path in geojson_files:
                self.process_file(file_path)

        self.final_report()

    def get_directories(self, base_dir):
        return [path for path in base_dir.iterdir() if path.is_dir()]

    def get_geojson_files(self, directory):
        return [
            file for file in directory.iterdir() if file.suffix.lower() == ".geojson"
        ]

    def process_file(self, file_path):
        success_created_count = 0
        success_updated_count = 0
        failure_count = 0

        try:
            with file_path.open() as infile:
                data = json.load(infile)
                for feature in data["features"]:
                    result = self.process_feature(feature)
                    if result == "created":
                        success_created_count += 1
                        self.total_created += 1
                    elif result == "updated":
                        success_updated_count += 1
                        self.total_updated += 1
                    else:
                        failure_count += 1
                        self.total_failed += 1
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f"An error occurred processing file {file_path}: {e}")
            )

        self.report_results(
            file_path, success_created_count, success_updated_count, failure_count
        )

    def process_feature(self, feature):
        properties = feature.get("properties", {})
        missing_fields = [
            field
            for field in ["name", "region_code", "country_code"]
            if field not in properties
        ]
        if missing_fields:
            self.stdout.write(
                self.style.WARNING(
                    f"Missing fields in properties: {', '.join(missing_fields)}"
                )
            )
            return "failed"

        name = properties.get("name")
        region_code = properties.get("region_code")
        country_code = properties.get("country_code")

        # Ensure country_code is 2 characters long
        country_code = country_code[:2] if country_code else None

        if not all([name, region_code, country_code]):
            self.stdout.write(
                self.style.ERROR("Name, region_code, and country_code are required.")
            )
            return "failed"

        # Clean up name
        name = re.sub(r"[^\w\s,.]", "", name).strip()

        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Country with code {country_code} does not exist.")
            )
            return "failed"

        defaults = {
            "name": name,
            "country": country,
            "geometry": GEOSGeometry(json.dumps(feature.get("geometry")))
            if feature.get("geometry")
            else None,
        }

        try:
            _obj, created = Region.objects.update_or_create(
                code=region_code,
                defaults=defaults,
            )
        except (IntegrityError, DataError, OperationalError) as e:
            self.stdout.write(
                self.style.ERROR(f"Database error processing region {region_code}: {e}")
            )
            return "failed"
        else:
            return "created" if created else "updated"

    def report_results(self, file_path, created, updated, failed):
        self.stdout.write(self.style.SUCCESS(f"File processed: {file_path}"))
        self.stdout.write(self.style.SUCCESS(f"Successfully created {created} zones."))
        self.stdout.write(self.style.SUCCESS(f"Successfully updated {updated} zones."))
        self.stdout.write(self.style.ERROR(f"Failed to process {failed} zones."))

    def final_report(self):
        self.stdout.write(
            self.style.SUCCESS(
                f"\n==============\nTotal zones created: {self.total_created}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f"Total zones updated: {self.total_updated}")
        )
        self.stdout.write(self.style.ERROR(f"Total zones failed: {self.total_failed}"))
