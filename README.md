# Mailer

> Dead-simple mailer micro-service for static websites

[![Github Tag](https://img.shields.io/github/tag/rclement/mailer.svg)](https://github.com/rclement/mailer/releases/latest)
[![GitHub Action CI/CD](https://github.com/rclement/mailer/workflows/Mailer%20CI/CD/badge.svg)](https://github.com/rclement/mailer/actions?query=workflow%3A%22Mailer+CI%2FCD%22)
[![Coverage Status](https://img.shields.io/codecov/c/github/rclement/mailer)](https://codecov.io/gh/rclement/mailer)
[![License](https://img.shields.io/github/license/rclement/mailer)](https://github.com/rmnclmnt/mailer/blob/master/LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/rmnclmnt/mailer.svg)](https://hub.docker.com/r/rmnclmnt/mailer)

A free and open-source software alternative to contact form services such as FormSpree,
to integrate a contact form seamlessly within your next static website!

When building static websites and [JAMStack](https://jamstack.org/) web applications,
the need for a contact form arises pretty often but requires some server-side processing.
`mailer` provides a dead-simple micro-service (usable as a serverless function) for this purpose,
enabling one to receive e-mails from a simple form using a single AJAX request.

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
