# Mailer

> Dead-simple mailer micro-service for static websites

[![Docker Pulls](https://img.shields.io/docker/pulls/rmnclmnt/mailer.svg)](https://hub.docker.com/r/rmnclmnt/mailer)
[![Github Tag](https://img.shields.io/github/tag/rclement/mailer.svg)](https://github.com/rclement/mailer/releases/latest)
[![GitHub Action CI/CD](https://github.com/rclement/mailer/workflows/Mailer%20CI/CD/badge.svg)](https://github.com/rclement/mailer/actions?query=workflow%3A%22Mailer+CI%2FCD%22)
[![Coverage Status](https://coveralls.io/repos/github/rclement/mailer/badge.svg?branch=master)](https://coveralls.io/github/rclement/mailer)

When building static websites, everyone needs a contact form, but that requires some server-side processing.
`mailer` provides a dead-simple micro-service (usable as a serverless function) for this purpose,
enabling one to send mails from a simple form using a single AJAX request:

```js
axios.post('https://mailer.domain.me/api/mail', {
  email: 'john@doe.com',
  name: 'John Doe',
  subject: 'Contact',
  message: 'Hey there! Up for a coffee?',
  honeypot: '',
  recaptcha: 'azertyuiopqsdfghjklmwxcvbn'
})
```

Create a free [Sendgrid](https://sendgrid.com) account (allows up to 100 mails per day forever)
and deploy with the [Zeit Now 2.0](https://zeit.co) serverless platform within minutes!

Proudly made using the [FastAPI](https://fastapi.tiangolo.com) ASGI framework.


## Features

- Self-hostable micro-service
- Docker and serverless support
- Unicode message support
- Swagger OpenAPI documentation
- CORS domain validation
- Spam-bot filtering with honeypot field
- Google ReCaptcha v2 validation
- Sentry crash reporting
- Only Sendgrid back-end supported (for now)


## Building

```
pipenv install -d
pipenv run pre-commit install --config .pre-commit-config.yml
pipenv run inv qa
```


## Running locally

1. Set environment variables:
    ```
    cp .env.example .env
    edit .env
    ```

2. Run dev server:
    ```
    uvicorn mailer.app:app --host 0.0.0.0 --port 8000
    ```

3. Try it:
    ```
    http GET http://localhost:8000/
    http POST http://localhost:8000/api/mail \
        Origin:http://localhost:8000 \
        email="john@doe.com" \
        name="John Doe" \
        subject="Test" \
        message="Hello" \
        honeypot=""
    ```

4. Open the Swagger OpenAPI documentation at `http://localhost:8000/docs`


## Deploying

### Configuration

The following environment variables are available:

| Variable | Default | Format | Description |
|----------|:-------:|:------:|-------------|
| `SENDER_EMAIL` | `""` | `no-reply@domain.me` | E-mail address to send e-mail from
| `TO_EMAIL` | `""` | `contact@domain.me` | E-mail address of the recipient
| `TO_NAME` | `""` | `My Name` | Name of the recipient
| `MAILER_PROVIDER` | `""` | {`sendgrid`} | Mailer back-end provider
| `SENDGRID_API_KEY` | `""` | `string` | Sendgrid secret API key
| `SENDGRID_SANDBOX` | `false` | {`false`, `true`} | Enable Sendgrid sandbox for testing purposes (does not send e-mails)
| `CORS_ORIGINS` | `'[]'` | `'["https://domain.me", "https://mydomain.me"]'` | (optional) List (JSON string) of authorized origins for CORS origins and Origin request header validation
| `RECAPTCHA_SECRET_KEY` | `""` | `string` | (optional) Google ReCaptcha v2 secret key
| `SENTRY_DSN` | `""` | `string` | (optional) Sentry crash reporting DSN

### Docker Hub deployment

```
pipenv run inv docker-deploy -u <username> -p <password> -r <repository> -t <tag>
```

### Zeit Now

1. Deploy `mailer` as a Lambda:

    ```
    now secrets add mailer-sendgrid-api-key xxxx
    now secrets add mailer-recaptcha-secret-key zzzz
    now \
        -e SENDER_EMAIL="no-reply@domain.me" \
        -e TO_EMAIL="name@domain.com" \
        -e TO_NAME="My Name" \
        -e MAILER_PROVIDER="sendgrid" \
        -e SENDGRID_API_KEY=@mailer-sendgrid-api-key \
        -e CORS_ORIGINS='["https://domain.com"]' \
        -e RECAPTCHA_SECRET_KEY=@mailer-recaptcha-secret-key \
        -e SENTRY_DSN="azerty"
    ```

2. (optional) add external domain to `now`:

    ```
    now domain add <domain.com>
    ```

    which will output `<token>`

3. With your DNS provider, add the following entries:

    ```
    TXT _now <token>
    CNAME <sub.domain.com> alias.zeit.co
    ```

4. Add the alias to `now`:

    ```
    now alias <sub.domain.com>
    ```

Note: if using CloudFlare, refer to the [documentation](https://zeit.co/docs/v1/guides/how-to-use-cloudflare).


## License

The MIT License (MIT)

Copyright (c) 2018 Romain Clement