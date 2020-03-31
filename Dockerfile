FROM python:3.8.2-alpine

RUN set -ex && pip install --upgrade pip && pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex \
    && apk add --virtual .build-deps build-base gcc musl-dev python3-dev libffi-dev openssl-dev \
    && pipenv install --deploy --system \
    && apk del .build-deps

COPY . /app

EXPOSE 5000

ENTRYPOINT ["honcho", "start"]
CMD ["web"]
