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
  -r local.txt

FROM python AS python-run-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
  sudo \
  git \
  bash-completion \
  nano \
  ssh \
  libpq-dev \
  wait-for-it \
  gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 dev-user \
  && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
  && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
  && chmod 0440 /etc/sudoers.d/dev-user

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY ./compose/prod/django/entrypoint /entrypoint
COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /entrypoint \
    && chmod +x /entrypoint \
    && sed -i 's/\r$//g' /start \
    && chmod +x /start

COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]
