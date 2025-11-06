FROM python:3.12.11-slim-bookworm AS builder

ENV APP_USER=app
ENV APP_ROOT=/${APP_USER}

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

RUN mkdir -p ${APP_ROOT}
WORKDIR ${APP_ROOT}
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-cache --no-install-project --no-editable
COPY . ./
RUN uv sync --locked --no-dev --no-editable

FROM python:3.12.11-slim-bookworm AS final

ENV APP_USER=app
ENV APP_GROUP=app
ENV APP_ROOT=/${APP_USER}
ENV HOST=0.0.0.0
ENV PORT=5000
ENV PATH="${APP_ROOT}/.venv/bin:$PATH"

RUN mkdir -p ${APP_ROOT}
WORKDIR ${APP_ROOT}
RUN groupadd -r ${APP_GROUP} && useradd --no-log-init -r -g ${APP_GROUP} ${APP_USER}
RUN chown -R ${APP_USER}:${APP_GROUP} ${APP_ROOT}

COPY --from=builder --chown=app:app ${APP_ROOT} ${APP_ROOT}
USER ${APP_USER}

EXPOSE ${PORT}

ENTRYPOINT ["honcho", "start"]
CMD ["web"]
