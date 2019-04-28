from invoke import task


app_path = "mailer"
tests_path = "tests"


@task
def test(ctx):
    cmd = f"py.test -v --cov={app_path} --cov-report term-missing tests"
    ctx.run(cmd, pty=True)


@task
def safety(ctx):
    cmd = "safety check"
    ctx.run(cmd)


@task
def lint(ctx):
    cmd = f"black --check {app_path} {tests_path}"
    ctx.run(cmd)


@task
def reformat(ctx):
    cmd = f"black {app_path} {tests_path}"
    ctx.run(cmd)


@task(test, safety, lint)
def qa(ctx):
    pass


@task
def docker_deploy(ctx, username=None, password=None, repository=None, tag="latest"):
    if username and password and repository and tag:
        cmd = f"echo {password} | docker login -u {username} --password-stdin"
        ctx.run(cmd)

        cmd = f"docker build -t {username}/{repository}:{tag} ."
        ctx.run(cmd)

        cmd = f"docker push {username}/{repository}:{tag}"
        ctx.run(cmd)
