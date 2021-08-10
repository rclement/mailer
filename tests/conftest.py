import os
import pytest

from typing import Generator
from fastapi import FastAPI
from responses import RequestsMock
from starlette.testclient import TestClient


# ------------------------------------------------------------------------------


os.environ["APP_ENVIRONMENT"] = "testing"
os.environ["SENDER_EMAIL"] = "no-reply@test.com"
os.environ["TO_EMAIL"] = "contact@test.com"
os.environ["TO_NAME"] = "Test"
os.environ["SMTP_HOST"] = "localhost"
os.environ["SMTP_PORT"] = "587"
os.environ["SMTP_TLS"] = "true"
os.environ["SMTP_SSL"] = "false"
os.environ["SMTP_USER"] = "user"
os.environ["SMTP_PASSWORD"] = "password"
os.environ["FORCE_HTTPS"] = "false"
os.environ["CORS_ORIGINS"] = "[]"
os.environ["RECAPTCHA_SECRET_KEY"] = ""
os.environ["PGP_PUBLIC_KEY"] = ""
os.environ["SENTRY_DSN"] = ""


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def responses() -> Generator[RequestsMock, None, None]:
    with RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture(scope="function")
def app() -> FastAPI:
    from mailer import create_app

    return create_app(None)


@pytest.fixture(scope="function")
def app_client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client
