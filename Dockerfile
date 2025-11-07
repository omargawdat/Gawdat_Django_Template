# Define an alias for the specific python version used in this file
# Pin UV version to prevent breaking changes (uv is pre-1.0)
FROM ghcr.io/astral-sh/uv:0.8.23-python3.13-trixie-slim AS python

# Python build stage
FROM python AS python-build-stage

# Only keep is_local as build argument since it affects build-time behavior
ARG is_local

# Validate required build argument
RUN if [ -z "$is_local" ]; then \
    echo "ERROR: is_local build argument must be explicitly set to 'true' or 'false'" && exit 1; \
fi

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

# UV environment variables for optimization
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    libgdal-dev \
    git \
    gettext \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies based on environment
# Use cache mount for faster rebuilds
# First sync: install dependencies only (no project)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    if [ "$is_local" = "true" ]; then \
        echo "Installing LOCAL dependencies (base + dev)" && \
        uv sync --frozen --no-install-project --group dev; \
    else \
        echo "Installing PRODUCTION dependencies (base + production)" && \
        uv sync --frozen --no-install-project --group production --no-dev; \
    fi

# Copy application code
COPY . ${APP_HOME}

# Second sync: install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    if [ "$is_local" = "true" ]; then \
        uv sync --frozen --group dev; \
    else \
        uv sync --frozen --group production --no-dev; \
    fi

# Set PATH to use .venv
ENV PATH="${APP_HOME}/.venv/bin:$PATH"

# Copy all entrypoint scripts
COPY ./scripts/docker-entrypoint /scripts/entrypoint
COPY ./scripts/docker-entrypoint.local /scripts/docker-entrypoint.local
COPY ./scripts/docker-entrypoint.dev /scripts/docker-entrypoint.dev
COPY ./scripts/docker-entrypoint.prod /scripts/docker-entrypoint.prod
RUN sed -i 's/\r$//g' /scripts/entrypoint /scripts/docker-entrypoint.* && \
    chmod +x /scripts/entrypoint /scripts/docker-entrypoint.*

# Python run stage
FROM python:3.13-slim-trixie AS python-run-stage

ARG is_local
ARG APP_HOME=/app

WORKDIR ${APP_HOME}

# Create application user
RUN groupadd -r django && useradd -r -g django -u 1000 -s /bin/false django

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    libgdal-dev \
    gettext \
    wait-for-it \
    git \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copy all entrypoint scripts
COPY --chown=django:django ./scripts/docker-entrypoint /scripts/entrypoint
COPY --chown=django:django ./scripts/docker-entrypoint.local /scripts/docker-entrypoint.local
COPY --chown=django:django ./scripts/docker-entrypoint.dev /scripts/docker-entrypoint.dev
COPY --chown=django:django ./scripts/docker-entrypoint.prod /scripts/docker-entrypoint.prod
RUN sed -i 's/\r$//g' /scripts/entrypoint /scripts/docker-entrypoint.* && \
    chmod +x /scripts/entrypoint /scripts/docker-entrypoint.*

# Copy the application from the builder stage
COPY --from=python-build-stage --chown=django:django ${APP_HOME} ${APP_HOME}

# Make django owner of the WORKDIR
RUN chown -R django:django ${APP_HOME}

# Place executables in the environment at the front of the path
ENV PATH="${APP_HOME}/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    IS_LOCAL=${is_local}

USER django

ENTRYPOINT ["/scripts/entrypoint"]

# Metadata
LABEL maintainer="your-email@example.com" \
      version="2.0" \
      description="Django application image with uv package manager"
