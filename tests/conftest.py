import os
import pytest


# ------------------------------------------------------------------------------


os.environ["APP_ENVIRONMENT"] = "testing"
os.environ["SENDER_EMAIL"] = "no-reply@test.com"
os.environ["TO_EMAIL"] = "contact@test.com"
os.environ["TO_NAME"] = "Test"
os.environ["MAILER_PROVIDER"] = "sendgrid"
os.environ["SENDGRID_API_KEY"] = "1234567890"
os.environ["SENDGRID_SANDBOX"] = "true"
os.environ["CORS_ORIGINS"] = "[]"
os.environ["RECAPTCHA_SECRET_KEY"] = ""
os.environ["SENTRY_DSN"] = ""


# ------------------------------------------------------------------------------


@pytest.fixture(scope="session")
def faker():
    from faker import Faker

    Faker.seed(1234)
    faker_instance = Faker()

    return faker_instance


@pytest.fixture(scope="function")
def responses():
    import responses

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture(scope="function")
def app_client():
    from starlette.testclient import TestClient
    from mailer import create_app

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
