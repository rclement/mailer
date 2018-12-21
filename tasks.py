from invoke import task


app_path = "mailer"
tests_path = "tests"


@task
def test(ctx):
    cmd = 'py.test -v --cov={app_path} --cov-report term-missing tests'.format(
        app_path=app_path
    )
    ctx.run(cmd, pty=True)


@task
def safety(ctx):
    cmd = 'safety check'
    ctx.run(cmd)


@task
def lint(ctx):
    cmd = 'flake8 --ignore E501 {app_path} {tests_path}'.format(
        app_path=app_path, tests_path=tests_path
    )
    ctx.run(cmd)


@task
def reformat(ctx):
    cmd = 'black {app_path} {tests_path}'.format(
        app_path=app_path, tests_path=tests_path
    )
    ctx.run(cmd)


@task(test, safety, lint)
def qa(ctx):
    pass


@task
def docker_deploy(ctx, username=None, password=None, repository=None, tag='latest'):
    if username and password and repository and tag:
        cmd = 'echo {password} | docker login -u {username} --password-stdin'.format(
            username=username, password=password
        )
        ctx.run(cmd)

        cmd = 'docker build -t {username}/{repository} .'.format(
            username=username, repository=repository
        )
        ctx.run(cmd)

        cmd = 'docker tag {username}/{repository} {username}/{repository}:{tag}'.format(
            username=username, repository=repository, tag=tag
        )
        ctx.run(cmd)

        cmd = 'docker push {username}/{repository}:{tag}'.format(
            username=username, repository=repository, tag=tag
        )
        ctx.run(cmd)
