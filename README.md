# Mailer

Simple mailer micro-service for static websites

[![Build Status Travis-CI](https://travis-ci.org/rclement/mailer.svg)](https://travis-ci.org/rclement/mailer)
[![Coverage Status](https://coveralls.io/repos/github/rclement/mailer/badge.svg?branch=develop)](https://coveralls.io/github/rclement/mailer?branch=develop)


## Build

```
pipenv install -d
pipenv run inv qa
```


## Deployment

### Docker Hub deployment

```
pipenv run docker-deploy -u <username> -p <password> -r <repository> -t <tag>
```

### Zeit Now

1. Deploy `mailer` as Docker-based app:

    ```
    now secrets add secret-key xxxx
    now secrets add sendgrid-api-key xxxx
    now \
        -e SERVER_NAME="sub.domain.com" \
        -e PREFERRED_URL_SCHEME="https" \
        -e SECRET_KEY="@secret-key" \
        -e TO_EMAIL="name@domain.com" \
        -e TO_NAME="My Name" \
        -e CORS_ORIGINS="https://domain.com" \
        -e MAILER_SERVICE="sendgrid" \
        -e SENDGRID_API_KEY="@sendgrid-api-key" \
    ```

2. (optional) add external domain to `now`:

    ```
    now domain add --external <domain.com>
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