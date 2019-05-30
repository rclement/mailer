FROM python:3.7.3-alpine

RUN set -ex && pip install --upgrade pip && pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex \
    && apk add --virtual .build-deps build-base gcc python-dev libffi-dev \
    && pipenv install --deploy --system \
    && apk del .build-deps

COPY . /app

EXPOSE 5000

ENTRYPOINT ["honcho", "start"]
CMD ["web"]
