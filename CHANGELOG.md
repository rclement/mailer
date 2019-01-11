# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
- Update .env.example
- Update default route rate-limiting rule to 10 per hour

## [0.1.0] - 2018-12-21
### Added
- Initial release of `mailer`
- Sendgrid mailing provider support

[Unreleased]: https://github.com/rclement/mailer/compare/0.4.0...HEAD
[0.4.0]: https://github.com/rclement/mailer/compare/0.2.0...0.4.0
[0.3.0]: https://github.com/rclement/mailer/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/rclement/mailer/compare/0.1.0...0.2.0
