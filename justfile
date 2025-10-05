# Django Template Justfile
# Common development commands for the project

# Default recipe - show available commands
default:
    @just --list

# ============================================================================
# Development Environment
# ============================================================================

# Install all dependencies locally with uv
install:
    uv sync --group dev --group test --group typing --group lint

# Update all dependencies to latest versions
update:
    uv lock --upgrade
    @echo "✅ Dependencies updated. Run 'just build' to rebuild containers."

# Clean all caches and build artifacts
clean:
    docker compose -f docker-compose.local.yml down -v
    docker volume prune -f
    rm -rf .venv .ruff_cache .mypy_cache .pytest_cache htmlcov .coverage
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    @echo "✅ Cleaned all caches and build artifacts"

# ============================================================================
# Docker Management
# ============================================================================

# Build Docker containers
build:
    docker compose -f docker-compose.local.yml build

# Start development environment
up:
    docker compose -f docker-compose.local.yml up -d

# Stop development environment
down:
    docker compose -f docker-compose.local.yml down

# Restart development environment
restart:
    docker compose -f docker-compose.local.yml restart

# View logs (follow mode)
logs service="django":
    docker compose -f docker-compose.local.yml logs -f {{service}}

# Rebuild and restart (full refresh)
rebuild:
    docker compose -f docker-compose.local.yml up --build -d

# ============================================================================
# Django Management Commands
# ============================================================================

# Run Django management command
manage *args:
    docker compose -f docker-compose.local.yml run --rm django python manage.py {{args}}

# Create and apply database migrations
migrate:
    docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

# Create new migrations
makemigrations *args:
    docker compose -f docker-compose.local.yml run --rm django python manage.py makemigrations {{args}}

# Create superuser
createsuperuser:
    docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser

# Open Django shell
shell:
    docker compose -f docker-compose.local.yml run --rm django python manage.py shell

# Open Django shell plus (requires django-extensions)
shell-plus:
    docker compose -f docker-compose.local.yml run --rm django python manage.py shell_plus

# Run Django development server (alternative to docker compose up)
runserver:
    docker compose -f docker-compose.local.yml run --rm --service-ports django python manage.py runserver 0.0.0.0:8000

# Load seed data
seed:
    docker compose -f docker-compose.local.yml run --rm django python manage.py seed_db

# ============================================================================
# Database Management
# ============================================================================

# Reset database (WARNING: destroys all data)
db-reset:
    docker compose -f docker-compose.local.yml down -v
    docker compose -f docker-compose.local.yml up -d postgres
    sleep 3
    @just migrate
    @echo "✅ Database reset complete"

# Open PostgreSQL shell
db-shell:
    docker compose -f docker-compose.local.yml exec postgres psql -U postgres -d mydatabase

# Backup database
db-backup:
    @echo "Creating database backup..."
    docker compose -f docker-compose.local.yml exec postgres pg_dump -U postgres mydatabase > backup_$(date +%Y%m%d_%H%M%S).sql
    @echo "✅ Database backup created"

# ============================================================================
# Testing
# ============================================================================

# Run all tests
test *args:
    docker compose -f docker-compose.local.yml run --rm django pytest {{args}}

# Run tests with coverage
test-cov:
    docker compose -f docker-compose.local.yml run --rm django pytest --cov --cov-report=html --cov-report=term

# Run specific test file or directory
test-file path:
    docker compose -f docker-compose.local.yml run --rm django pytest {{path}}

# ============================================================================
# Code Quality
# ============================================================================

# Run ruff linter
lint:
    uv run ruff check .

# Run ruff formatter
format:
    uv run ruff format .

# Run both linter and formatter
lint-all:
    uv run ruff check . --fix
    uv run ruff format .

# Run type checking with mypy
typecheck:
    uv run mypy .

# Run all code quality checks
check: lint typecheck
    @echo "✅ All code quality checks passed"

# ============================================================================
# Security
# ============================================================================

# Scan dependencies for vulnerabilities
audit:
    @echo "Scanning dependencies for security vulnerabilities..."
    uv export --no-hashes | pip-audit -r /dev/stdin

# Run security checks (bandit)
security:
    uv run bandit -r apps/ config/ common/ -ll

# Check for secrets in code
secrets:
    docker compose -f docker-compose.local.yml run --rm django python manage.py check --deploy

# ============================================================================
# Pre-commit
# ============================================================================

# Install pre-commit hooks
pre-commit-install:
    pre-commit install
    pre-commit install --hook-type commit-msg
    pre-commit install --hook-type pre-push

# Run pre-commit on all files
pre-commit-all:
    pre-commit run --all-files

# Update pre-commit hooks
pre-commit-update:
    pre-commit autoupdate

# ============================================================================
# Utilities
# ============================================================================

# Show Docker container status
ps:
    docker compose -f docker-compose.local.yml ps

# Enter Django container shell
bash:
    docker compose -f docker-compose.local.yml exec django bash

# Enter PostgreSQL container shell
bash-db:
    docker compose -f docker-compose.local.yml exec postgres bash

# Check uv.lock is in sync with pyproject.toml
lock-check:
    uv lock --check

# Show outdated packages
outdated:
    @echo "Checking for outdated packages..."
    @uv tree --outdated || echo "All packages are up to date"

# Generate requirements.txt for legacy tools
export-requirements:
    uv export --no-hashes --format requirements-txt > requirements.txt
    @echo "✅ Generated requirements.txt"
