import pytest

from http import HTTPStatus


@pytest.fixture(scope="function")
def enable_cors_origins(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", '["https://domain.me"]')


@pytest.fixture(scope="function")
def enable_recaptcha(monkeypatch):
    monkeypatch.setenv("RECAPTCHA_SECRET_KEY", "1234567890")


@pytest.fixture(scope="function")
def mock_requests_post(mocker):
    return mocker.patch("requests.post", autospec=True)


@pytest.fixture(scope="function")
def mock_recaptcha_success(faker, mocker, mock_requests_post):
    def json():
        return {
            "success": True,
            "challenge_ts": faker.iso8601(),
            "hostname": faker.hostname(),
        }

    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.side_effect = json

    return mock_requests_post


@pytest.fixture(scope="function")
def mock_recaptcha_missing_secret(faker, mocker, mock_requests_post):
    def json():
        return {"success": False, "error-codes": ["missing-input-secret"]}

    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.side_effect = json

    return mock_requests_post


@pytest.fixture(scope="function")
def mock_recaptcha_missing_response(faker, mocker, mock_requests_post):
    def json():
        return {"success": False, "error-codes": ["missing-input-response"]}

    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.side_effect = json

    return mock_requests_post


@pytest.fixture(scope="function")
def mock_sendgrid_request(mocker):
    return mocker.patch("python_http_client.Client._make_request")


@pytest.fixture(scope="function")
def mock_sendgrid_success(mocker, mock_sendgrid_request):
    from http import HTTPStatus

    ret_val = mocker.Mock()
    ret_val.getcode.return_value = HTTPStatus.ACCEPTED
    ret_val.read.return_value = ""
    ret_val.info.return_value = ""

    mock_sendgrid_request.return_value = ret_val

    return mock_sendgrid_request


@pytest.fixture(scope="function")
def mock_sendgrid_unauthorized(mocker, mock_sendgrid_request):
    from http import HTTPStatus
    from python_http_client import exceptions as phce

    ret_val = mocker.Mock()
    ret_val.code = HTTPStatus.UNAUTHORIZED
    ret_val.reason = ""
    ret_val.hdrs = ""
    ret_val.read.return_value = ""

    mock_sendgrid_request.side_effect = phce.UnauthorizedError(ret_val)

    return mock_sendgrid_request


@pytest.fixture(scope="function")
def params_success(faker):
    return {
        "email": faker.email(),
        "name": faker.name(),
        "subject": faker.text(max_nb_chars=100),
        "message": faker.text(max_nb_chars=200),
        "honeypot": "",
    }


# ------------------------------------------------------------------------------


def test_get_api_info_success(app_client):
    from mailer import __about__

    response = app_client.get("/api/")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["name"] == __about__.__title__
    assert data["version"] == __about__.__version__
    assert data["api_version"] == "v1"


# ------------------------------------------------------------------------------


def test_send_mail_success(app_client, mock_sendgrid_success, params_success):
    params = params_success

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["email"] == params["email"]
    assert data["name"] == params["name"]
    assert data["subject"] == params["subject"]
    assert data["message"] == params["message"]
    assert data["honeypot"] == params["honeypot"]


def test_send_mail_unauthorized(app_client, mock_sendgrid_unauthorized, params_success):
    params = params_success

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_send_mail_none(app_client, mock_sendgrid_success):
    params = {}

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_empty_fields(app_client, mock_sendgrid_success):
    params = {"email": "", "name": "", "subject": "", "message": "", "honeypot": ""}

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_empty_email(app_client, mock_sendgrid_success, params_success):
    params = params_success
    params["email"] = ""

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_empty_name(app_client, mock_sendgrid_success, params_success):
    params = params_success
    params["name"] = ""

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_empty_subject(app_client, mock_sendgrid_success, params_success):
    params = params_success
    params["subject"] = ""

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_empty_message(app_client, mock_sendgrid_success, params_success):
    params = params_success
    params["message"] = ""

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_bad_email(app_client, mock_sendgrid_success, params_success):
    params = params_success
    params["email"] = "joe@doe"

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_too_long_name(
    app_client, mock_sendgrid_success, params_success, faker
):
    params = params_success
    params["name"] = faker.text(max_nb_chars=100)

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_too_long_subject(
    app_client, mock_sendgrid_success, params_success, faker
):
    params = params_success
    params["subject"] = faker.text(max_nb_chars=400)

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_too_long_message(
    app_client, mock_sendgrid_success, params_success, faker
):
    params = params_success
    params["message"] = faker.text(max_nb_chars=400)

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_non_empty_honeypot(
    app_client, mock_sendgrid_success, params_success, faker
):
    params = params_success
    params["honeypot"] = faker.text()

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_matching_cors_origin(
    enable_cors_origins, app_client, mock_sendgrid_success, params_success
):
    params = params_success

    headers = {"Origin": "https://domain.me"}

    response = app_client.post("/api/mail", json=params, headers=headers)
    assert response.status_code == HTTPStatus.OK


def test_send_mail_unmatched_cors_origin(
    enable_cors_origins, app_client, mock_sendgrid_success, params_success
):
    params = params_success

    headers = {"Origin": "https://unknown-domain.me"}

    response = app_client.post("/api/mail", json=params, headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_send_mail_recaptcha_success(
    enable_recaptcha,
    app_client,
    mock_sendgrid_success,
    mock_recaptcha_success,
    params_success,
    faker,
):
    params = params_success
    params["recaptcha"] = faker.pystr()

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.OK


def test_send_mail_recaptcha_no_response(
    enable_recaptcha,
    app_client,
    mock_sendgrid_success,
    mock_recaptcha_missing_response,
    params_success,
):
    params = params_success
    params["recaptcha"] = ""

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
