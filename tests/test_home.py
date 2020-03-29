from http import HTTPStatus


def test_get_api_info_success(app_client):
    from mailer import __about__

    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK

    data = response.text
    assert __about__.__version__ in data
    assert app_client.app.url_path_for("swagger_ui_html") in data
    assert app_client.app.url_path_for("redoc_html") in data
