from invoke import task


app_path = "mailer"
tests_path = "tests"


@task
def audit(ctx):
    ctx.run("safety check", pty=True)


@task
def lint(ctx):
    ctx.run(f"flake8 {app_path} {tests_path}", pty=True)


@task
def static_check(ctx):
    ctx.run(f"mypy --strict {app_path}", pty=True)


@task
def security_check(ctx):
    ctx.run(f"bandit -v -r {app_path}", pty=True)


@task
def test(ctx):
    ctx.run(f"py.test -v --cov={app_path} --cov={tests_path} --cov-branch --cov-report=term-missing {tests_path}", pty=True)


@task(audit, lint, static_check, security_check, test)
def qa(ctx):
    pass


@task
def reformat(ctx):
    ctx.run(f"black {app_path} {tests_path}", pty=True)
