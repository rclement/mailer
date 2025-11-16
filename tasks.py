from invoke import task


app_path = "mailer"
tests_path = "tests"


@task
def audit(ctx):
    ctx.run("pip-audit", pty=True)


@task
def lint(ctx):
    ctx.run(f"ruff check {app_path} {tests_path}", pty=True)


@task
def typing(ctx):
    ctx.run(f"mypy --strict {app_path} {tests_path}", pty=True)


@task
def vuln(ctx):
    ctx.run(f"bandit -v -r {app_path}", pty=True)


@task
def test(ctx):
    ctx.run(
        f"py.test -v --cov={app_path} --cov={tests_path} --cov-branch --cov-report=term-missing {tests_path}",
        pty=True,
    )


@task(audit, lint, typing, vuln, test)
def qa(ctx):
    pass


@task
def format(ctx):
    ctx.run(f"ruff format {app_path} {tests_path}", pty=True)


@task
def generate_pgp_key_pair(ctx, name, email, filename):
    from tests import utils

    key = utils.generate_pgp_key_pair(name, email)

    with open(f"{filename}.pub.asc", mode="w") as f:
        f.write(str(key.pubkey))

    with open(f"{filename}.asc", mode="w") as f:
        f.write(str(key))


@task
def encrypt_pgp_message(ctx, public_key_file_path, message):
    from tests import utils

    with open(public_key_file_path, mode="r") as f:
        public_key = f.read()

    encrypted_message = utils.encrypt_pgp_message(public_key, message)

    print(encrypted_message)


@task
def decrypt_pgp_message(ctx, private_key_file_path, encrypted_file_path):
    from tests import utils

    with open(private_key_file_path, mode="r") as f:
        private_key = f.read()

    with open(encrypted_file_path, mode="r") as f:
        encrypted_message = f.read()

    message = utils.decrypt_pgp_message(private_key, encrypted_message)

    print(message)
