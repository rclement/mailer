# Mailer

> Dead-simple mailer micro-service for static websites

[![Docker Pulls](https://img.shields.io/docker/pulls/rmnclmnt/mailer.svg)](https://hub.docker.com/r/rmnclmnt/mailer)
[![Github Tag](https://img.shields.io/github/tag/rclement/mailer.svg)](https://github.com/rclement/mailer/releases/latest)
[![Build Status Travis-CI](https://travis-ci.org/rclement/mailer.svg?branch=master)](https://travis-ci.org/rclement/mailer)
[![Coverage Status](https://coveralls.io/repos/github/rclement/mailer/badge.svg?branch=master)](https://coveralls.io/github/rclement/mailer)

[![Deploy to now](https://deploy.now.sh/static/button.svg)](https://deploy.now.sh/?repo=https://github.com/rclement/mailer&env=TO_EMAIL&env=TO_NAME&env=CORS_ORIGINS&env=RECAPTCHA_ENABLED&env=RECAPTCHA_SITE_KEY&env=RECAPTCHA_SECRET_KEY&env=MAILER_SERVICE&env=SENDGRID_API_KEY)

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

Proudly made using the [Flask](http://flask.pocoo.org) micro-framework.


## Features

- Self-hostable micro-service
- Docker and serverless support
- Unicode message support
- Swagger OpenAPI documentation
- CORS domain validation
- Rate-limiting support
- Spam-bot filtering with honeypot field
- Google ReCaptcha v2 validation
- Sentry crash reporting
- Only Sendgrid back-end supported (for now)


## Building

```
pipenv install -d
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
    flask run
    ```

3. Try it:
    ```
    http GET http://localhost:5000/api/
    http POST http://localhost:5000/api/mail email="john@doe.com" name="John Doe" subject="Test" message="Hello"
    ```

4. Open the Swagger OpenAPI documentation at `http://localhost:5000/docs`


## Deploying

### Configuration

The following environment variables are available:

| Variable | Default | Format | Description |
|----------|:-------:|:------:|-------------|
| `SENDER_EMAIL` | `""` | `no-reply@domain.me` | E-mail address to send e-mail from
| `TO_EMAIL` | `""` | `contact@domain.me` | E-mail address of the recipient
| `TO_NAME` | `""` | `My Name` | Name of the recipient
| `MAILER_SERVICE` | `""` | {`sendgrid`} | Mailer back-end service
| `SENDGRID_API_KEY` | `""` | `string` | Sendgrid secret API key
| `SENDGRID_SANDBOX` | `false` | {`false`, `true`} | Enable Sendgrid sandbox for testing purposes (does not send e-mails)
| `CORS_ORIGINS` | `""` | `https://domain.me, https://mydomain.me` | (optional) List of comma-separated authorized CORS origins
| `RATELIMIT_ENABLED` | `false` | {`false`, `true`} | (optional) Enable rate-limiting for the API, based on IP address
| `RATELIMIT_DEFAULT` | `10 per hour` | cf. `flask-limiter` | (optional) Rate-limit per API end-point
| `RATELIMIT_APPLICATION` | `100 per day` | cf. `flask-limiter` | (optional) Rate-limit for all API end-points
| `RATELIMIT_STORAGE_URL` | `memory://` | cf. `flask-limiter` | (optional) Rate-limit storage URL
| `RATELIMIT_STRATEGY` | `moving-window` | cf. `flask-limiter` | (optional) Rate-limit strategy
| `RECAPTCHA_ENABLED` | `false` | {`false`, `true`} | (optional) Enable Google ReCaptcha v2 validation
| `RECAPTCHA_SITE_KEY` | `""` | `string` | (optional) Google ReCaptcha v2 site key
| `RECAPTCHA_SECRET_KEY` | `""` | `string` | (optional) Google ReCaptcha v2 secret key
| `SENTRY_ENABLED` | `false` | {`false`, `true`} | (optional) Enable Sentry crash reporting
| `SENTRY_DSN` | `""` | `string` | (optional) Sentry DSN

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
        -e TO_EMAIL="name@domain.com" \
        -e TO_NAME="My Name" \
        -e CORS_ORIGINS="https://domain.com" \
        -e RECAPTCHA_ENABLED="true" \
        -e RECAPTCHA_SITE_KEY="wxcvbn" \
        -e RECAPTCHA_SECRET_KEY="@mailer-recaptcha-secret-key" \
        -e MAILER_SERVICE="sendgrid" \
        -e SENDGRID_API_KEY="@mailer-sendgrid-api-key" \
        -e SENTRY_ENABLED="true" \
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