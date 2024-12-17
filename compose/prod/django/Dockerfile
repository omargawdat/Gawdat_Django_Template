FROM docker.io/python:3.12.7-slim-bookworm AS python

FROM python AS python-build-stage

WORKDIR /usr/src/app

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev \
  git \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r prod.txt

FROM python AS python-run-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR ${APP_HOME}

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev \
  gettext \
  wait-for-it \
  git \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY --chown=django:django ./compose/prod/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

COPY --chown=django:django ./compose/prod/django/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

COPY --chown=django:django . ${APP_HOME}

RUN chown -R django:django ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint"]
