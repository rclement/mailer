# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.10.3] - 2023-06-16
### Changed
- Use Python 3.11.4
- Update dependencies

## [0.10.2] - 2022-08-28
### Changed
- Use Python 3.10.6
- Update dependencies

## [0.10.1] - 2022-02-18
### Changed
- Use Python 3.9.10
- Fix form link in homepage template
- Remove duplicate honeypot validation
- Move documentation to https://rclement.github.io/mailer/
- Disable Renovate dependency dashboard
- Update dependencies

## [0.10.0] - 2021-09-18
### Added
- New API endpoint for URL-encoded form requests
- Type hints for tests

### Changed
- Use Python 3.9.7
- Update dependencies

## [0.9.1] - 2021-06-17
### Added
- 1-click deployment buttons to README and documentation (Vercel and Heroku)

### Changed
- Use Python 3.8.10
- Update dependencies

## [0.9.0] - 2021-05-01
### Added
- Allow to force HTTPS redirect using `FORCE_HTTPS` (enabled by default)

### Changed
- Use Python 3.8.9
- Use `python-slim` instead of `python-alpine` base for Docker image
- Use `mkdocs` for documentation
- Rename all Zeit Now references to Vercel
- Update dependencies

## [0.8.1] - 2020-05-21
### Added
- OpenAPI documentation for return model in `/api/` route

### Changed
- Use Python 3.8.3
- Update dependencies
- More robust CORS origins testing
- Stricter `mypy` rules

### Fixed
- Better handling of `.env` file loading for development and testing

## [0.8.0] - 2020-04-11
### Changed
- Use Python 3.8.2
- Use [FastAPI](https://fastapi.tiangolo.com) instead of [Flask](https://flask.palletsprojects.com)
- Renamed API parameter `recaptcha` to `g-recaptcha-response` (default name from Google ReCaptcha)
- Set maximum message length to 1000 characters
- Disable Swagger UI in production
- Licensed under AGPLv3

### Added
- [Docsify](https://docsify.js.org) documentation
- Simple homepage with API documentation link
- SMTP mailing backend support (all `SMTP_*` configurations)
- PGP encryption support using PGP/MIME (with optional contact PGP public key attachment)
- Static typing analysis using [mypy](https://mypy.readthedocs.io)
- Security checks using [bandit](https://bandit.readthedocs.io)
- Exhaustive testing
- Simple examples (ajax, ajax with recaptcha, ajax with pgp)
- GitHub Action workflows support
- Security notice in `SECURITY.md`

### Removed
- **BREAKING**: removed rate-limiting feature (all `RATELIMIT_*` configurations)
- **BREAKING**: removed mailer provider feature (`MAILER_PROVIDER` configuration)
- **BREAKING**: removed sendgrid provider feature (all `SENDGRID_*` configurations)
- Removed `RECAPTCHA_SITE_KEY` from configuration
- Removed `RECAPTCHA_ENABLED` from configuration (automatically enabled when `RECAPTCHA_SECRET_KEY` is set)
- Removed `SENTRY_ENABLED` from configuration (automatically enabled when `SENTRY_DSN` is set)
- Travis-CI support

### Fixed
- Use non-root user in `Dockerfile`
- Use allowlist mode for `.nowignore`

## [0.7.1] - 2019-07-22
### Changed
- Update Python dependencies

### Added
- Use `flake8` as linter, `black` as code formatter
- Use `pre-commit` for git hooks support

## [0.7.0] - 2019-06-23
### Fixed
- Force HTTPS protocol even behind reverse-proxies

### Changed
- Update Python dependencies
- Rename `mailer.services` package to `mailer.providers`
- BREAKING: rename `MAILER_SERVICE` config to `MAILER_PROVIDER`

### Added
- BREAKING: add `SENDER_EMAIL` config to specify the e-mail to send from (e.g. `no-reply@domain.me`)

## [0.6.2] - 2019-05-30
### Changed
- Update Python dependencies
- Migrate to Zeit Now official Python WSGI builder

## [0.6.1] - 2019-04-29
### Security
- Update Python dependencies
- Fix `jinja2` vulnerability ([CVE-2019-10906](https://nvd.nist.gov/vuln/detail/CVE-2019-10906))
- Fix `urllib3` vulnerability ([CVE-2019-11324](https://nvd.nist.gov/vuln/detail/CVE-2019-11324))

### Fixed
- Fix `sendgrid` >= `6.0.0` breaking changes

### Added
- Travis-CI deployment to Zeit Now serverless platform

## [0.6.0] - 2019-03-28
### Security
- Fix `webargs` vulnerability ([CVE-2019-9710](https://nvd.nist.gov/vuln/detail/CVE-2019-9710))

### Fixed
- Werkzeug deprecation warning for `ProxyFix`

### Added
- Swagger OpenAPI documentation
- Sentry crash reporting support

### Removed
- `SECRET_KEY` secret config (unused)
- `SERVER_NAME` config (unused)

## [0.5.0] - 2019-01-20
### Added
- Google ReCaptcha v2 validation
- Disabling rate-limiting

### Changed
- README.md with complete list of environment variables for configuration

## [0.4.0] - 2019-01-10
### Added
- Zeit Now 2.0 serverless/lambda deployment compatibility!

### Changed
- Update Python dependencies
- API info endpoint (`/api`) exempted from rate-limiting and returns some more information

## [0.3.0] - 2019-01-10
### Added
- Add optional `honeypot` param for spam-bot protection

## [0.2.0] - 2019-01-09
### Added
- Add CHANGELOG.md

### Changed
- Update Python dependencies
- Update .example.env
- Update default route rate-limiting rule to 10 per hour

## [0.1.0] - 2018-12-21
### Added
- Initial release of `mailer`
- Sendgrid mailing provider support

[Unreleased]: https://github.com/rclement/mailer/compare/0.10.3...HEAD
[0.10.3]: https://github.com/rclement/mailer/compare/0.10.2...0.10.3
[0.10.2]: https://github.com/rclement/mailer/compare/0.10.1...0.10.2
[0.10.1]: https://github.com/rclement/mailer/compare/0.10.0...0.10.1
[0.10.0]: https://github.com/rclement/mailer/compare/0.9.1...0.10.0
[0.9.1]: https://github.com/rclement/mailer/compare/0.9.0...0.9.1
[0.9.0]: https://github.com/rclement/mailer/compare/0.8.1...0.9.0
[0.8.1]: https://github.com/rclement/mailer/compare/0.8.0...0.8.1
[0.8.0]: https://github.com/rclement/mailer/compare/0.7.1...0.8.0
[0.7.1]: https://github.com/rclement/mailer/compare/0.7.0...0.7.1
[0.7.0]: https://github.com/rclement/mailer/compare/0.6.2...0.7.0
[0.6.2]: https://github.com/rclement/mailer/compare/0.6.1...0.6.2
[0.6.1]: https://github.com/rclement/mailer/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/rclement/mailer/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/rclement/mailer/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/rclement/mailer/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/rclement/mailer/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/rclement/mailer/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/rclement/mailer/releases/tag/0.1.0
