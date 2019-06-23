import os
import pytest


# ------------------------------------------------------------------------------


os.environ["FLASK_ENV"] = "testing"
os.environ["SENDER_EMAIL"] = "no-reply@test.com"
os.environ["TO_EMAIL"] = "contact@test.com"
os.environ["TO_NAME"] = "Test"
os.environ["RECAPTCHA_ENABLED"] = "false"
os.environ["MAILER_SERVICE"] = "sendgrid"
os.environ["SENDGRID_API_KEY"] = "1234567890"
os.environ["SENDGRID_SANDBOX"] = "true"


# ------------------------------------------------------------------------------


@pytest.fixture(scope="session")
def app(request):
    from mailer import wsgi

    _app = wsgi.app

    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()
