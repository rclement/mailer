# Deployment

You will need to choose:

- A mailing provider
- A cloud provider

Most mailing providers offer a generous free-tier to get started
([Sendgrid](https://sendgrid.com), [Mailjet](https://mailjet.com), etc.)
and allow usage via SMTP.

Regarding cloud providers, you can start deploying with [Vercel](https://vercel.com)
serverless platform within minutes! But any PaaS and/or Docker-compatible provider will do!

## Configuration

The following environment variables are available:

| Variable               | Default  |                      Format                      | Description                                                                                                                                   |
| ---------------------- | :------: | :----------------------------------------------: | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `SENDER_EMAIL`         |   `""`   |               `no-reply@domain.me`               | (**required**) E-mail address to send e-mail from                                                                                             |
| `TO_EMAIL`             |   `""`   |               `contact@domain.me`                | (**required**) E-mail address of the recipient                                                                                                |
| `TO_NAME`              |   `""`   |                    `My Name`                     | (**required**) Name of the recipient                                                                                                          |
| `SMTP_HOST`            |   `""`   |                 `smtp.host.com`                  | (**required**) SMTP host URL                                                                                                                  |
| `SMTP_PORT`            |   `""`   |                      `587`                       | (**required**) SMTP host port                                                                                                                 |
| `SMTP_TLS`             |   `""`   |                      `true`                      | (**required**) SMTP host use TLS (mutually exclusive with SSL)                                                                                |
| `SMTP_SSL`             |   `""`   |                     `false`                      | (**required**) SMTP host use SSL (mutually exclusive with TLS)                                                                                |
| `SMTP_USER`            |   `""`   |                   `smtp-user`                    | (**required**) SMTP host user                                                                                                                 |
| `SMTP_PASSWORD`        |   `""`   |                 `smtp-password`                  | (**required**) SMTP host password (or API key)                                                                                                |
| `FORCE_HTTPS`          | `'true'` |                     `'true'`                     | (**optional**) Force HTTPS redirect                                                                                                           |
| `CORS_ORIGINS`         |  `'[]'`  | `'["https://domain.me", "https://mydomain.me"]'` | (**optional**) List (JSON string) of authorized origins for CORS origins and Origin request header validation                                 |
| `RECAPTCHA_SECRET_KEY` |   `""`   |                     `string`                     | (**optional**) Google ReCaptcha v2 secret key                                                                                                 |
| `PGP_PUBLIC_KEY`       |   `""`   |                     `base64`                     | (**optional**) Base64-encoded PGP public key to encrypt e-mails with before sending to SMTP backend (generate with `cat <pub.asc> \| base64`) |
| `SENTRY_DSN`           |   `""`   |                     `string`                     | (**optional**) Sentry crash reporting DSN                                                                                                     |

## Verification

In order to verify that `mailer` is properly deployed, go to the domain or
sub-domain pointing to your deployment (e.g. `https://mailer.domain.me`).

You should be able to display the homepage and the API documentation
(e.g. `https://mailer.domain.me/redoc`).
If either the homepage or the API documentation do not display properly,
check the logs according to your deployment method.

If something feels fishy, you can always post an issue on
[GitHub](https://github.com/rclement/mailer/issues).

## Serverless (e.g. Vercel)

The easiest way to get started with serverless deployment is to use [Vercel](https://vercel.com).
You will need to create a Vercel account and to install the [Vercel CLI](https://vercel.com/cli).

1. From the `mailer` codebase, create a new project on Vercel: `vercel`

2. Create the secrets containing sensitive information for your configuration:
```bash
vercel secrets add mailer-smtp-password xxxx
vercel secrets add mailer-recaptcha-secret-key zzzz
```

3. Deploy as a function (with your appropriate configuration):
```bash
vercel \
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
    -e PGP_PUBLIC_KEY='LS0...==' \
    -e SENTRY_DSN="azerty"
```

## PaaS (e.g. Heroku, CleverCloud)

The easiest way to get started with PaaS deployment is to use [Heroku](https://heroku.com).
You will need to create a Heroku account and to install the
[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

1. Create a project on the Heroku dashboard and add your configuration in environment variables

2. Login to Heroku: `heroku login`

3. From the `mailer` codebase, add the Git remote: `heroku git:remote -a <my-mailer-app>`

4. Deploy: `git push heroku master:master`

Or you can also use the containerized version!

## Docker

The Docker image is publicly available on [Docker Hub](https://hub.docker.com/r/rmnclmnt/mailer).

All stable versions are automatically deployed and available after each release.
The `latest` tag will allow to retrieve non-stable changes

If you want to quickly try the Docker image:

```bash
docker run --env-file .env -p 5000:5000 rmnclmnt/mailer:latest
```

## VPS

If you're feeling nerdy or a bit old-school, you are more than welcome to
deploy `mailer` using a standard VPS from any cloud provider (AWS, OVH, etc.).

We still recommend you deploy `mailer` using the provided Docker image for
reproducibility reasons.

This kind of deployment will also require some extra steps, such as setting up:

- A reverse-proxy link [Nginx](https://www.nginx.com)
- Automatic SSL/TLS certificate generation using [Let's Encrypt](https://letsencrypt.org)
- A firewall with sensitive rules (only allow ports 80 and 443)
- Security policies (only allow SSH access using public key, disable root user over SSH, etc.)
- External intrusion protection using [fail2ban](https://www.fail2ban.org)
- etc.

If you do not know (nor want to know) how to perform this kind of setup, use more
developer-friendly deployment options!
