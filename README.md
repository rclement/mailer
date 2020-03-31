# Mailer

> Dead-simple mailer micro-service for static websites

[![Docker Pulls](https://img.shields.io/docker/pulls/rmnclmnt/mailer.svg)](https://hub.docker.com/r/rmnclmnt/mailer)
[![Github Tag](https://img.shields.io/github/tag/rclement/mailer.svg)](https://github.com/rclement/mailer/releases/latest)
[![GitHub Action CI/CD](https://github.com/rclement/mailer/workflows/Mailer%20CI/CD/badge.svg)](https://github.com/rclement/mailer/actions?query=workflow%3A%22Mailer+CI%2FCD%22)
[![Coverage Status](https://img.shields.io/codecov/c/github/rclement/mailer)](https://codecov.io/gh/rclement/mailer)

When building static websites, everyone needs a contact form, but that requires some server-side processing.
`mailer` provides a dead-simple micro-service (usable as a serverless function) for this purpose,
enabling one to send mails from a simple form using a single AJAX request:

```js
fetch('https://mailer.domain.me/api/mail', {
  method: 'POST',
  headers: {
      'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'john@doe.com',
    name: 'John Doe',
    subject: 'Contact',
    message: 'Hey there! Up for a coffee?',
    honeypot: '',
    'g-recaptcha-response': 'azertyuiopqsdfghjklmwxcvbn'
  })
})
```

All you need is to choose a mailing provider and a cloud provider!

Most mailing providers offer a generous free-tier to get started ([Sendgrid](https://sendgrid.com), [Mailjet](https://mailjet.com), etc.) and allow usage via SMTP.

Regarding cloud providers, you can start deploying with [Zeit Now 2.0](https://zeit.co) serverless platform within minutes!
But any PaaS and/or Docker-compatible provider will do!

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
- Any SMTP-compatible back-end is supported
- PGP encryption support using PGP/MIME

## Building

```
pipenv install -d
pipenv run pre-commit install --config .pre-commit-config.yml
pipenv run inv qa
```

## Running locally

1. Set environment variables:
    ```
    cp .example.env .env
    edit .env
    ```

2. Run dev server:
    ```
    pipenv run uvicorn mailer.app:app --host 0.0.0.0 --port 8000
    ```

3. Try it:
    ```
    http GET http://localhost:8000/
    http POST http://localhost:8000/api/mail \
        Origin:http://localhost:8000 \
        email="john@doe.com" \
        name="John Doe" \
        subject="Test 💫" \
        message="Hello 👋" \
        honeypot=""
    ```

4. Open the Swagger OpenAPI documentation at `http://localhost:8000/docs`

5. Run the examples:
    ```
    pipenv run python -m http.server 5000
    ```


## Deploying

### Configuration

The following environment variables are available:

| Variable | Default | Format | Description |
|----------|:-------:|:------:|-------------|
| `SENDER_EMAIL` | `""` | `no-reply@domain.me` | E-mail address to send e-mail from
| `TO_EMAIL` | `""` | `contact@domain.me` | E-mail address of the recipient
| `TO_NAME` | `""` | `My Name` | Name of the recipient
| `SMTP_HOST` | `""` | `smtp.host.com` | SMTP host URL
| `SMTP_PORT` | `""` | `587` | SMTP host port
| `SMTP_TLS` | `""` | `true` | SMTP host use TLS (mutually exclusive with SSL)
| `SMTP_SSL` | `""` | `false` | SMTP host use SSL (mutually exclusive with TLS)
| `SMTP_USER` | `""` | `smtp-user` | SMTP host user
| `SMTP_PASSWORD` | `""` | `smtp-password` | SMTP host password (or API key)
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
    now secrets add mailer-smtp-password xxxx
    now secrets add mailer-recaptcha-secret-key zzzz
    now \
        -e SENDER_EMAIL="no-reply@domain.me" \
        -e TO_EMAIL="name@domain.com" \
        -e TO_NAME="My Name" \
        -e SMTP_HOST="smtp.host.com" \
        -e SMTP_PORT="587" \
        -e SMTP_TLS="true" \
        -e SMTP_SSL="false" \
        -e SMTP_USER="smtp-user" \
        -e SMTP_PASSWORD=@mailer-smtp-password \
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

### Heroku

1. Login to Heroku: `heroku login`

2. Add the Git remote: `heroku git:remote -a <my-mailer-app>`

3. Deploy: `git push heroku master:master`

Or you can also use the containerized version!

## License

Licensed under GNU Affero General Public License v3.0 (AGPLv3)

Copyright (c) 2018 - present  Romain Clement