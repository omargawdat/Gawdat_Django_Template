#!/usr/bin/env python
# ruff: noqa
import os
import sys
from pathlib import Path


if __name__ == "__main__":
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    # This allows easy placement of apps within the interior
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "apps"))

    is_local = os.environ.get("IS_LOCAL", "true").lower() == "true"
    os.environ["DJANGO_SETTINGS_MODULE"] = (
        "config.settings.local" if is_local else "config.settings.prod"
    )

    execute_from_command_line(sys.argv)
