FROM python:3.8.2-alpine

ENV APP_USER=app
ENV APP_GROUP=app
ENV APP_ROOT=/home/${APP_USER}

RUN mkdir -p ${APP_ROOT}
WORKDIR ${APP_ROOT}

RUN set -ex && pip install --upgrade pip && pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex \
    && apk add --virtual .build-deps build-base gcc musl-dev python3-dev libffi-dev openssl-dev \
    && pipenv install --deploy --system \
    && apk del .build-deps

RUN addgroup -S ${APP_GROUP} && adduser ${APP_USER} -S -G ${APP_GROUP}
RUN chown -R ${APP_USER}:${APP_GROUP} ${APP_ROOT}
USER ${APP_USER}

COPY --chown=app:app . ${APP_ROOT}

ENV HOST 0.0.0.0
ENV PORT 5000

EXPOSE ${PORT}

ENTRYPOINT ["honcho", "start"]
CMD ["web"]
