# ruff: noqa
import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "apps"))

if os.environ.get("ENVIRONMENT") in ["development", "production", "staging"]:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
elif os.environ.get("ENVIRONMENT") == "local":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_wsgi_application()
