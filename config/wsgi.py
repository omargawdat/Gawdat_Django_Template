# ruff: noqa
import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "apps"))

# Choose settings based on environment variable
print(f"ENVIRONMENT: {os.environ.get('ENVIRONMENT')}")
if os.environ.get("ENVIRONMENT") in ["dev", "prod", "stag"]:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
elif os.environ.get("ENVIRONMENT") == "local":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
else:
    raise ValueError(
        f"Invalid or missing DJANGO_ENV. Got: {os.environ.get('DJANGO_ENV')}"
    )

application = get_wsgi_application()
