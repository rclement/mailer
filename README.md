# Mailer

> Dead-simple mailer micro-service for static websites

[![Github Tag](https://img.shields.io/github/tag/rclement/mailer.svg)](https://github.com/rclement/mailer/releases/latest)
[![CI/CD](https://github.com/rclement/mailer/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/rclement/mailer/actions/workflows/ci-cd.yml)
[![Coverage Status](https://img.shields.io/codecov/c/github/rclement/mailer)](https://codecov.io/gh/rclement/mailer)
[![License](https://img.shields.io/github/license/rclement/mailer)](https://github.com/rmnclmnt/mailer/blob/master/LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/rmnclmnt/mailer.svg)](https://hub.docker.com/r/rmnclmnt/mailer)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/git/external?repository-url=https://github.com/rclement/mailer&env=SENDER_EMAIL,TO_EMAIL,TO_NAME,SMTP_HOST,SMTP_PORT,SMTP_TLS,SMTP_SSL,SMTP_USER,SMTP_PASSWORD&envDescription=Configuration&envLink=https://rclement.github.io/mailer/deployment/#configuration)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/rclement/mailer)

A free and open-source software alternative to contact form services such as FormSpree,
to integrate a contact form seamlessly within your next static website!

When building static websites and [JAMStack](https://jamstack.org/) web applications,
the need for a contact form arises pretty often but requires some server-side processing.
`mailer` provides a dead-simple micro-service (usable as a serverless function) for this purpose,
enabling one to receive e-mails from a simple form using a single request, be it URL-encoded
or AJAX.

Proudly developed in Python using the [FastAPI](https://fastapi.tiangolo.com) ASGI framework.

## Features

- Self-hostable micro-service
- Docker and serverless support
- Unicode message support
- OpenAPI documentation (Swagger and ReDoc)
- CORS domain validation
- Spam-bot filtering with honeypot field
- Google ReCaptcha v2 validation
- Sentry crash reporting
- Any SMTP-compatible back-end is supported
- PGP encryption support using PGP/MIME

## License

Licensed under GNU Affero General Public License v3.0 (AGPLv3)

Copyright (c) 2018 - present  Romain Clement
