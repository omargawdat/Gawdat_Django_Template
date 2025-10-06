# Django Template Justfile
#
# First time setup:
#   just install && just up && just migrate && just createsuperuser
#
# Common workflows:
#   just rebuild     # After dependency changes
#   just test        # Run tests
#   just lint-all    # Fix code style

# Show all commands
default:
    @just --list

# ============================================================================
# 🚀 Quick Start
# ============================================================================

# Install dependencies
install:
    uv sync --group dev --group test --group typing --group lint

# Start all services
up:
    docker compose -f docker-compose.local.yml up -d

# Stop all services
down:
    docker compose -f docker-compose.local.yml down

# Rebuild and restart everything
rebuild:
    docker compose -f docker-compose.local.yml up --build -d

# View logs (usage: just logs [service])
logs service="django":
    docker compose -f docker-compose.local.yml logs -f {{service}}

# ============================================================================
# 🗄️ Database
# ============================================================================

# Apply migrations
migrate:
    docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

# Create migrations (usage: just makemigrations [app])
makemigrations *args:
    docker compose -f docker-compose.local.yml run --rm django python manage.py makemigrations {{args}}

# Reset database - DELETES ALL DATA!
db-reset:
    @echo "⚠️  Deleting all data in 3 seconds..."
    @sleep 3
    docker compose -f docker-compose.local.yml down -v
    docker compose -f docker-compose.local.yml up -d postgres
    @sleep 3
    @just migrate

# ============================================================================
# 🐍 Django
# ============================================================================

# Run management command (usage: just manage [command])
manage *args:
    docker compose -f docker-compose.local.yml run --rm django python manage.py {{args}}

# Create superuser
createsuperuser:
    docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser

# Open Django shell
shell:
    docker compose -f docker-compose.local.yml run --rm django python manage.py shell_plus

# Load seed data
seed:
    docker compose -f docker-compose.local.yml run --rm django python manage.py seed_db

# ============================================================================
# 🧪 Testing
# ============================================================================

# Run tests (usage: just test [-v] [-k test_name])
test *args:
    docker compose -f docker-compose.local.yml run --rm django pytest {{args}}

# Run tests with coverage
test-cov:
    docker compose -f docker-compose.local.yml run --rm django pytest --cov --cov-report=html --cov-report=term

# ============================================================================
# ✨ Code Quality
# ============================================================================

# Fix linting and format code
lint-all:
    uv run ruff check . --fix
    uv run ruff format .

# Check code style
lint:
    uv run ruff check .

# Format code
format:
    uv run ruff format .

# Type check
typecheck:
    uv run mypy .

# Run all checks
check: lint typecheck

# ============================================================================
# 📦 Dependencies
# ============================================================================

# Update all dependencies
update:
    uv lock --upgrade
    @echo "Run 'just rebuild' to apply changes"

# Show outdated packages
outdated:
    @uv tree --outdated || echo "All packages up to date"

# ============================================================================
# 🛠️ Utilities
# ============================================================================

# Show container status
ps:
    docker compose -f docker-compose.local.yml ps

# Open bash in Django container
bash:
    docker compose -f docker-compose.local.yml exec django bash

# Clean all artifacts and volumes
clean:
    docker compose -f docker-compose.local.yml down -v
    docker volume prune -f
    rm -rf .venv .ruff_cache .mypy_cache .pytest_cache htmlcov .coverage
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Setup pre-commit hooks
pre-commit-install:
    pre-commit install
    pre-commit install --hook-type commit-msg
    pre-commit install --hook-type pre-push

# Scan for security vulnerabilities
audit:
    uv export --no-hashes | pip-audit -r /dev/stdin
