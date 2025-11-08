# ================================
# Build Stage: Python Dependencies
# ================================
FROM python:3.13-slim-trixie AS python-build-stage

# Build arguments - only keep what affects build behavior
ARG is_local
ARG APP_HOME=/app
ARG UV_VERSION=0.8.23

# Validate required build argument
RUN if [ -z "$is_local" ]; then \
    echo "ERROR: is_local build argument must be explicitly set to 'true' or 'false'" && exit 1; \
    fi

# Set working directory
WORKDIR ${APP_HOME}

# UV environment variables for optimization
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_CACHE_DIR=/root/.cache/uv \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install build dependencies and UV in a single layer
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    libgdal-dev \
    gettext \
    curl \
    git \
    && curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

# Copy only dependency files first (better layer caching)
# These files change less frequently than application code
COPY pyproject.toml uv.lock ./

# Install Python dependencies based on environment
# Use cache mount for faster rebuilds
# First sync: dependencies only (no project installation)
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ "$is_local" = "true" ]; then \
        echo "Installing LOCAL dependencies (base + dev)" && \
        uv sync --frozen --no-install-project --group dev; \
    else \
        echo "Installing PRODUCTION dependencies (base + production)" && \
        uv sync --frozen --no-install-project --group production --no-dev; \
    fi

# Copy entrypoint scripts early (changes rarely)
COPY ./scripts/docker-entrypoint /scripts/entrypoint
COPY ./scripts/docker-entrypoint.local /scripts/docker-entrypoint.local
COPY ./scripts/docker-entrypoint.dev /scripts/docker-entrypoint.dev
COPY ./scripts/docker-entrypoint.prod /scripts/docker-entrypoint.prod

# Fix line endings and set permissions in one layer
RUN sed -i 's/\r$//g' /scripts/entrypoint /scripts/docker-entrypoint.* && \
    chmod +x /scripts/entrypoint /scripts/docker-entrypoint.*

# Copy application code LAST (changes most frequently)
# This maximizes Docker layer cache efficiency
COPY . ${APP_HOME}

# Second sync: install the project itself
# This uses the already-installed dependencies from the previous layer
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ "$is_local" = "true" ]; then \
        uv sync --frozen --group dev; \
    else \
        uv sync --frozen --group production --no-dev; \
    fi

# ================================
# Runtime Stage: Minimal Production Image
# ================================
FROM python:3.13-slim-trixie AS python-run-stage

ARG is_local
ARG APP_HOME=/app

# Environment labels for metadata
LABEL maintainer="your-email@example.com" \
      version="2.0" \
      description="Django application with uv package manager" \
      org.opencontainers.image.source="https://github.com/your-org/your-repo" \
      org.opencontainers.image.vendor="Your Organization"

WORKDIR ${APP_HOME}

# Create application user EARLY (best practice - do this before copying files)
# Using consistent UID helps with volume permissions
RUN groupadd -r django && \
    useradd -r -g django -u 1000 -s /bin/false django

# Install ONLY runtime dependencies (minimal surface area)
# Remove build tools to reduce image size and attack surface
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install --no-install-recommends -y \
    libpq5 \
    libgdal36 \
    gettext \
    wait-for-it \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

# Copy application and dependencies from build stage
# Use --chown to set ownership during copy (more efficient)
COPY --from=python-build-stage --chown=django:django ${APP_HOME} ${APP_HOME}

# Copy entrypoint scripts from build stage
COPY --from=python-build-stage --chown=django:django /scripts /scripts

# Set environment variables for runtime
ENV PATH="${APP_HOME}/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    IS_LOCAL=${is_local} \
    PYTHONPYCACHEPREFIX=/tmp/pycache


#HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
#    CMD python -c "import sys; from django.core.management import execute_from_command_line; execute_from_command_line(['manage.py', 'check', '--deploy'])" || exit 1

# Switch to non-root user for security
USER django

# Set entrypoint
ENTRYPOINT ["/scripts/entrypoint"]
