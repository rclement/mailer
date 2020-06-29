import pytest

from http import HTTPStatus


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def enable_production(monkeypatch):
    monkeypatch.setenv("APP_ENVIRONMENT", "production")


@pytest.fixture(scope="function")
def enable_force_https(monkeypatch):
    monkeypatch.setenv("FORCE_HTTPS", "true")


# ------------------------------------------------------------------------------


def test_get_homepage_success(app_client):
    from mailer import __about__

    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK

    data = response.text
    assert __about__.__title__ in data
    assert __about__.__version__ in data
    assert __about__.__description__ in data
    assert app_client.app.url_path_for("swagger_ui_html") in data
    assert app_client.app.url_path_for("redoc_html") in data


def test_get_homepage_production_success(enable_production, app_client):
    from mailer import __about__
    from starlette.routing import NoMatchFound

    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK

    data = response.text
    assert __about__.__title__ in data
    assert __about__.__version__ in data
    assert __about__.__description__ in data
    assert app_client.app.url_path_for("redoc_html") in data

    assert app_client.app.docs_url is None
    with pytest.raises(NoMatchFound):
        app_client.app.url_path_for("swagger_ui_html")


def test_get_homepage_https_redirect(enable_force_https, app_client):
    response = app_client.get("/", allow_redirects=False)
    assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT
