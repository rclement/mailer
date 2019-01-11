# Mailer

> Dead-simple mailer micro-service for static websites

[![Docker Pulls](https://img.shields.io/docker/pulls/rmnclmnt/mailer.svg)](https://hub.docker.com/r/rmnclmnt/mailer)
[![Github Tag](https://img.shields.io/github/tag/rclement/mailer.svg)](https://github.com/rclement/mailer/releases/latest)
[![Build Status Travis-CI](https://travis-ci.org/rclement/mailer.svg?branch=master)](https://travis-ci.org/rclement/mailer)
[![Coverage Status](https://coveralls.io/repos/github/rclement/mailer/badge.svg?branch=master)](https://coveralls.io/github/rclement/mailer)

[![Deploy to now](https://deploy.now.sh/static/button.svg)](https://deploy.now.sh/?repo=https://github.com/rclement/mailer&env=SECRET_KEY&env=TO_EMAIL&env=TO_NAME&env=CORS_ORIGINS&env=MAILER_SERVICE&env=SENDGRID_API_KEY)

When building static websites, everyone needs a contact form, but that requires some server-side processing.
`mailer` provides a dead-simple micro-service (usable as a serverless function) for this purpose,
enabling one to send mails from a simple form using a single AJAX request:

```js
axios.post('https://mailer.domain.me/api/mail', {
  email: 'john@doe.com',
  name: 'John Doe',
  subject: 'Contact',
  message: 'Hey there! Up for a coffee?',
  honeypot: ''
})
```

Create a free [Sendgrid](https://sendgrid.com) account (allows up to 100 mails per day forever)
and deploy with the [Zeit Now 2.0](https://zeit.co) serverless platform within minutes!

Proudly made using the [Flask](http://flask.pocoo.org) micro-framework.


## Building

```
pipenv install -d
pipenv run inv qa
```


## Running locally

1. Generate `flask` secret key:
    ```
    flask run generate-secret-key
    ```

2. Set environment variables:
    ```
    cp .env.example .env
    edit .env
    ```

3. Run dev server:
    ```
    flask run
    ```

4. Try it:
    ```
    http GET localhost:5000/api/
    http POST localhost:5000/api/mail email="john@doe.com" name="John Doe" subject="Test" message="Hello"
    ```


## Deploying

### Docker Hub deployment

```
pipenv run inv docker-deploy -u <username> -p <password> -r <repository> -t <tag>
```

### Zeit Now

1. Deploy `mailer` as a Lambda:

    ```
    now secrets add mailer-secret-key $(flask generate-secret-key)
    now secrets add mailer-sendgrid-api-key xxxx
    now \
        -e SECRET_KEY="@mailer-secret-key" \
        -e TO_EMAIL="name@domain.com" \
        -e TO_NAME="My Name" \
        -e CORS_ORIGINS="https://domain.com" \
        -e MAILER_SERVICE="sendgrid" \
        -e SENDGRID_API_KEY="@mailer-sendgrid-api-key" \
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