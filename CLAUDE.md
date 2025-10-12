# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django REST API template project with a modular app structure and comprehensive CI/CD pipeline. The project
uses Docker for local development and includes payment systems and location services.

## Package Management

This project uses **uv** package manager with dependencies defined in `pyproject.toml`:

- **pyproject.toml** - Single source of truth for all dependencies
  - `[project.dependencies]` - Core/base dependencies (Django, DRF, etc.)
  - `[project.optional-dependencies]` - Production extras (gunicorn, sentry, S3)
  - `[dependency-groups]` - PEP 735 groups (dev, test, typing, lint)
- **uv.lock** - Lockfile with exact versions and SHA256 hashes (auto-generated)

### Managing Dependencies

```bash
# Add a new dependency
uv add package-name

# Add to dev group
uv add --group dev package-name

# Remove a dependency
uv remove package-name

# Update specific package
uv lock --upgrade-package django

# Update all packages
uv lock --upgrade
```

## Development Commands

### Local Development Setup

```bash
# Copy environment variables
cp dummy.env .env

# Start development environment with Docker Compose
docker-compose -f docker-compose.local.yml up --build -d

# Run Django management commands
docker compose -f docker-compose.local.yml run --rm django python manage.py [command]

# Examples:
docker compose -f docker-compose.local.yml run --rm django python manage.py makemigrations
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
```

## Architecture

### Project Structure

- `config/` - Django settings and configuration
    - `settings/` - Environment-specific settings (base.py, local.py, prod.py, test.py)
    - `integrations/` - Third-party service integrations (DRF, Sentry, FCM, etc.)
    - `helpers/` - Utility modules for authentication, exception handling, OAuth adapters
- `apps/` - Django applications
    - `users/` - User management and authentication
    - `location/` - Country/location services
    - `payment/` - Payment processing
    - `channel/` - Communication channels
    - `appInfo/` - Application information
- `common/` - Shared utilities and base classes
    - `base/` - Base admin classes and inline configurations
    - `insights/` - Dashboard and analytics utilities
    - `views/` - Common view mixins and utilities

### App Structure Example

Each Django app follows a consistent structure. Example from `apps/location/`:

```
apps/location/
├── models/
│   ├── __init__.py
│   ├── address.py
│   ├── country.py
│   └── region.py
├── api/
│   ├── address/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── region/
│       ├── serializers.py
│       ├── urls.py
│       └── views.py
├── migrations/
├── admin.py
├── apps.py
└── tests.py
```

### Key Configuration

- Multi-language support (Arabic/English)

### Environment Variables

we define environment variables in `config/helpers/env.py`
