# Build stage
FROM docker.io/python:3.12.7-slim-bookworm AS python-build-stage

# Only keep is_local as build argument since it affects build-time behavior
ARG is_local

# Validate required build argument
RUN if [ -z "$is_local" ]; then \
    echo "ERROR: is_local build argument must be explicitly set to 'true' or 'false'" && exit 1; \
fi

WORKDIR /usr/src/app

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY ./requirements .

# Install dependencies into wheels
RUN if [ "$is_local" = "true" ]; then \
    echo "Building with LOCAL dependencies" && \
    pip wheel --wheel-dir /usr/src/app/wheels -r local.txt; \
else \
    echo "Building with PRODUCTION dependencies" && \
    pip wheel --wheel-dir /usr/src/app/wheels -r prod.txt; \
fi

# Run stage
FROM docker.io/python:3.12.7-slim-bookworm AS python-run-stage

# Pass is_local from build stage to runtime
ARG is_local
ENV IS_LOCAL=$is_local


# Set common environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Create application user
RUN groupadd -r django && useradd -r -g django -u 1000 -s /bin/false django

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    wait-for-it \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY --from=python-build-stage /usr/src/app/wheels /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

# Create and configure scripts directory
RUN mkdir -p /scripts && chown django:django /scripts

# Copy combined entrypoint script
COPY --chown=django:django ./scripts/docker-entrypoint /scripts/entrypoint
RUN sed -i 's/\r$//g' /scripts/entrypoint && chmod +x /scripts/entrypoint

# Copy application code
COPY --chown=django:django . /app

# Switch to non-root user
USER django

ENTRYPOINT ["/scripts/entrypoint"]

# Metadata
LABEL maintainer="your-email@example.com" \
      version="1.0" \
      description="Django application image"
