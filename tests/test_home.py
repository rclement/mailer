import pytest

from http import HTTPStatus
from fastapi import FastAPI
from starlette.testclient import TestClient


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def enable_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENVIRONMENT", "production")


@pytest.fixture(scope="function")
def enable_force_https(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORCE_HTTPS", "true")


# ------------------------------------------------------------------------------


def test_get_homepage_success(app: FastAPI, app_client: TestClient) -> None:
    from mailer import __about__

    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK

    data = response.text
    assert __about__.__title__ in data
    assert __about__.__version__ in data
    assert __about__.__description__ in data
    assert app.url_path_for("swagger_ui_html") in data
    assert app.url_path_for("redoc_html") in data


def test_get_homepage_production_success(
    enable_production: None, app: FastAPI, app_client: TestClient
) -> None:
    from mailer import __about__
    from starlette.routing import NoMatchFound

    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK

    data = response.text
    assert __about__.__title__ in data
    assert __about__.__version__ in data
    assert __about__.__description__ in data
    assert app.url_path_for("redoc_html") in data

    assert app.docs_url is None
    with pytest.raises(NoMatchFound):
        app.url_path_for("swagger_ui_html")


def test_get_homepage_https_redirect(
    enable_force_https: None, app_client: TestClient
) -> None:
    response = app_client.get("/", follow_redirects=False)
    assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT
