# Package Management Migration Guide

## Summary

This project has been migrated from traditional `requirements/*.txt` files to a modern `pyproject.toml` + `uv` package manager setup.

## What Changed

### Files Modified
- ✅ `pyproject.toml` - Now contains all dependencies using PEP 621 & PEP 735 standards
- ✅ `Dockerfile` - Rewritten to use uv package manager
- ✅ `docker-compose.local.yml` - Added `.venv` volume exclusion
- ✅ `.dockerignore` - Added `.venv` and `requirements/` exclusions
- ✅ `.pre-commit-config.yaml` - Updated ruff version to match pyproject.toml

### Files Created
- ✅ `uv.lock` - Lockfile with exact versions and security hashes (388KB)

### Files Deleted
- ❌ `requirements/base.txt`
- ❌ `requirements/local.txt`
- ❌ `requirements/prod.txt`
- ❌ `requirements/` directory

## New Dependency Structure

### pyproject.toml Structure

```toml
[project]
dependencies = [...]  # Core 56 packages (base dependencies)

[project.optional-dependencies]
prod = [...]  # Production extras (gunicorn, sentry, S3, etc.)

[dependency-groups]  # PEP 735
dev = [...]     # Development tools (debug-toolbar, extensions)
test = [...]    # Testing (pytest, coverage, factory-boy)
typing = [...]  # Type checking (mypy, stubs)
lint = [...]    # Code quality (ruff, djlint, pre-commit)
```

## How to Use

### Local Development

```bash
# All commands remain the same!
docker-compose -f docker-compose.local.yml up --build -d
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
```

### Adding Dependencies

**Old way:**
```bash
# Edit requirements/base.txt
echo "new-package==1.0.0" >> requirements/base.txt
docker-compose up --build
```

**New way (faster):**
```bash
# Add to pyproject.toml
uv add new-package==1.0.0

# Or add to dev group
uv add --group dev new-dev-package

# Rebuild
docker-compose -f docker-compose.local.yml up --build
```

### Updating Dependencies

```bash
# Update a specific package
uv lock --upgrade-package django

# Update all packages
uv lock --upgrade

# Rebuild
docker-compose -f docker-compose.local.yml up --build
```

### Removing Dependencies

```bash
uv remove package-name
docker-compose -f docker-compose.local.yml up --build
```

## Benefits

✅ **10-100x faster** - uv is written in Rust
✅ **Single source of truth** - All deps in pyproject.toml
✅ **Security** - Lockfile includes SHA256 hashes
✅ **PEP compliant** - Standard Python packaging (PEP 621, 735)
✅ **Better caching** - Docker layers cache more efficiently
✅ **Easier updates** - `uv lock --upgrade` updates everything
✅ **Dependency groups** - Clear separation of dev/test/lint/prod

## Docker Details

### Build Process (Aligned with cookiecutter-django Pattern)

The Dockerfile uses a **multi-stage build** pattern similar to cookiecutter-django/my_awesome_project:

1. **Python alias stage** - Defines base `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` image

2. **python-build-stage** - Builds the application
   - Sets UV optimization flags: `UV_COMPILE_BYTECODE=1`, `UV_LINK_MODE=copy`, `UV_PYTHON_DOWNLOADS=0`
   - **First sync**: Installs dependencies only (`--no-install-project`)
     - Local: `--group dev --group test --group typing --group lint`
     - Prod: `--extra prod --no-dev`
   - Copies application code
   - **Second sync**: Installs the project itself
   - Uses Docker cache mounts for `/root/.cache/uv` (faster rebuilds)
   - Uses bind mounts for `pyproject.toml` and `uv.lock` (better layer caching)

3. **python-run-stage** - Clean runtime image
   - Uses fresh `python:3.12.9-slim-bookworm` (no uv bloat)
   - Copies entire `/app` from build stage (includes `.venv`)
   - Sets `PATH=/app/.venv/bin:$PATH`
   - Runs as non-root `django` user

### Why .venv Volume Exclusion?

```yaml
volumes:
  - /app/.venv  # Anonymous volume for .venv (MUST BE FIRST)
  - .:/app:z    # Mount source code
```

**Order matters!** Docker processes volumes top-to-bottom:
1. First line creates anonymous volume for `/app/.venv`
2. Second line mounts local code to `/app`
3. Result: Code is mounted, but `.venv` from image is preserved

**Why this works:**
- Anonymous volume has priority over bind mount for that specific path
- Code changes are live-reloaded (hot-reload in development)
- Installed packages remain intact from Docker image

## Troubleshooting

### Issue: Module not found
```bash
# Ensure .venv volume is FIRST in docker-compose
volumes:
  - /app/.venv  # Must be first!
  - .:/app:z
```

### Issue: Permission denied
```bash
# Rebuild image completely
docker-compose -f docker-compose.local.yml build --no-cache django
```

### Issue: Lockfile out of sync
```bash
# Regenerate lockfile
uv lock --upgrade
docker-compose -f docker-compose.local.yml up --build
```

## CI/CD Notes

If you have GitHub Actions or other CI:

```yaml
# Old
- run: pip install -r requirements/prod.txt

# New
- run: |
    pip install uv
    uv sync --frozen --extra prod --no-dev
```

## Questions?

- uv docs: https://docs.astral.sh/uv/
- PEP 735: https://peps.python.org/pep-0735/
- PEP 621: https://peps.python.org/pep-0621/
