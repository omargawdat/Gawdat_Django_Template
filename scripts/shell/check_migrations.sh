#!/usr/bin/env bash
set -e

# This script checks:
# 1. If all migration files are tracked and committed by git.
# 2. If makemigrations would create new migrations (indicating you forgot to run it).
# 3. If there are unapplied migrations (indicating you forgot to run migrate).
#
# This version is adapted for a Docker environment, where Django commands
# are run in a container:
# docker compose -f docker-compose.local.yml run --rm django python manage.py ...
#
# Adjust paths, compose files, and service names as needed.

COMPOSE_CMD="docker compose -f docker-compose.local.yml"
DJANGO_CMD="$COMPOSE_CMD run --rm django python manage.py"

echo "Checking for untracked or modified migration files..."
UNTRACKED_MIGRATIONS=$(git ls-files --others --exclude-standard | grep 'migrations/' || true)
MODIFIED_MIGRATIONS=$(git ls-files --modified | grep 'migrations/' || true)

if [ -n "$UNTRACKED_MIGRATIONS" ] || [ -n "$MODIFIED_MIGRATIONS" ]; then
    echo "ERROR: There are untracked or uncommitted migration files:"
    if [ -n "$UNTRACKED_MIGRATIONS" ]; then
        echo "Untracked:"
        echo "$UNTRACKED_MIGRATIONS"
    fi
    if [ -n "$MODIFIED_MIGRATIONS" ]; then
        echo "Modified:"
        echo "$MODIFIED_MIGRATIONS"
    fi
    echo "Please add/commit these migrations to version control."
    exit 1
else
    echo "All migration files are tracked and up-to-date in version control."
fi

echo "Checking if new migrations are needed..."
# Check directly in the if statement:
if ! $DJANGO_CMD makemigrations --dry-run --check >/dev/null 2>&1; then
    echo "ERROR: New migrations are needed but haven't been created."
    echo "Run '$DJANGO_CMD makemigrations' to create them."
    exit 1
else
    echo "No new migrations needed."
fi

echo "Checking for unapplied migrations..."
if UNAPPLIED=$($DJANGO_CMD migrate --plan | grep '^\[ \]') 2>/dev/null; then
    echo "ERROR: There are unapplied migrations:"
    echo "$UNAPPLIED"
    echo "Run '$DJANGO_CMD migrate' to apply them."
    exit 1
else
    echo "All migrations are applied."
fi

echo "All checks passed. Your migrations are up-to-date and applied."
