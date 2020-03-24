import os

from invoke import task


app_path = "mailer"
tests_path = "tests"


@task
def test(ctx):
    ctx.run(f"py.test -v --cov={app_path} --cov-report term-missing {tests_path}", pty=True)


@task
def audit(ctx):
    ctx.run("safety check")


@task
def lint(ctx):
    ctx.run(f"flake8 {app_path} {tests_path}")


@task
def reformat(ctx):
    ctx.run(f"black {app_path} {tests_path}", pty=True)


@task
def static_check(ctx):
    ctx.run(f"mypy --strict {app_path}", pty=True)


@task(test, audit, lint, static_check)
def qa(ctx):
    pass


@task
def docker_deploy(ctx, username=None, password=None, repository=None, tag="latest"):
    if username and password and repository and tag:
        cmd = f"echo {password} | docker login -u {username} --password-stdin"
        ctx.run(cmd)

        cmd = f"docker pull {username}/{repository}:latest"
        ctx.run(cmd)

        cmd = f"docker build -t {username}/{repository}:{tag} ."
        ctx.run(cmd)

        cmd = f"docker push {username}/{repository}:{tag}"
        ctx.run(cmd)


@task
def now_deploy(ctx, now_token=None, now_project=None, now_target=None, now_alias=None):
    # TODO: use Pydantic Settings

    now_token = now_token or os.environ.get("NOW_TOKEN", None)
    now_project = now_project or os.environ.get("NOW_PROJECT", None)
    now_target = now_target or os.environ.get("NOW_TARGET", "staging")
    now_alias = now_alias or os.environ.get("NOW_ALIAS", None)

    sender_email = os.environ.get("MAILER_SENDER_EMAIL", None)
    to_email = os.environ.get("MAILER_TO_EMAIL", None)
    to_name = os.environ.get("MAILER_TO_NAME", None)
    mailer_provider = os.environ.get("MAILER_MAILER_PROVIDER", None)
    sendgrid_api_key = os.environ.get("MAILER_SENDGRID_API_KEY", None)
    cors_origins = os.environ.get("MAILER_CORS_ORIGINS", "")
    recaptcha_secret_key = os.environ.get("MAILER_RECAPTCHA_SECRET_KEY", None)

    sentry_dsn = os.environ.get("MAILER_SENTRY_DSN", None)

    use_now_alias = now_alias and now_target == "production"
    now_token_arg = f"--token '{now_token}'" if now_token else ""
    now_target_arg = f"--target '{now_target}'" if now_target else ""

    use_sendgrid = mailer_provider == "sendgrid" and sendgrid_api_key
    sendgrid_api_key_name = "mailer-sendgrid-api-key"
    sendgrid_api_key_arg = (
        f"-e SENDGRID_API_KEY='@{sendgrid_api_key_name}'" if use_sendgrid else ""
    )

    recaptcha_secret_key_name = "mailer-recaptcha-secret-key"
    recaptcha_secret_key_arg = (
        f"-e RECAPTCHA_SECRET_KEY='@{recaptcha_secret_key_name}'" if recaptcha_secret_key else ""
    )

    if now_project and to_email and to_name and mailer_provider:
        if use_sendgrid:
            sendgrid_secret = (
                f"now secrets"
                f" {now_token_arg}"
                f" add 'mailer-sendgrid-api-key' '{sendgrid_api_key}'"
            )
            ctx.run(sendgrid_secret, echo=True, warn=True)

        if recaptcha_secret_key:
            recaptcha_secret = (
                f"now secrets"
                f" {now_token_arg}"
                f" add '{recaptcha_secret_key_name}' '{recaptcha_secret_key}'"
            )
            ctx.run(recaptcha_secret, echo=True, warn=True)

        deploy = (
            "now deploy"
            f" {now_token_arg}"
            f" --name '{now_project}'"
            f" {now_target_arg}"
            f" -e SENDER_EMAIL='{sender_email}'"
            f" -e TO_EMAIL='{to_email}'"
            f" -e TO_NAME='{to_name}'"
            f" -e MAILER_PROVIDER='{mailer_provider}'"
            f" {sendgrid_api_key_arg}"
            f" -e CORS_ORIGINS='{cors_origins}'"
            f" {recaptcha_secret_key_arg}"
            f" -e SENTRY_DSN='{sentry_dsn}'"
        )

        if ctx.run(deploy, echo=True) and use_now_alias:
            alias = "now alias" f" {now_token_arg}" f" set '{now_alias}'"
            ctx.run(alias, echo=True)
