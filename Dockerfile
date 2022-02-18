FROM python:3.9.10-slim

ENV APP_USER=app
ENV APP_GROUP=app
ENV APP_ROOT=/home/${APP_USER}

RUN mkdir -p ${APP_ROOT}
WORKDIR ${APP_ROOT}

RUN set -ex && pip install --upgrade pip && pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex && pipenv install --deploy --system

RUN groupadd -r ${APP_GROUP} && useradd --no-log-init -r -g ${APP_GROUP} ${APP_USER}
RUN chown -R ${APP_USER}:${APP_GROUP} ${APP_ROOT}
USER ${APP_USER}

COPY --chown=app:app . ${APP_ROOT}

ENV HOST 0.0.0.0
ENV PORT 5000

EXPOSE ${PORT}

ENTRYPOINT ["honcho", "start"]
CMD ["web"]
