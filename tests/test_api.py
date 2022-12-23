import os
import pytest

from base64 import urlsafe_b64encode
from http import HTTPStatus
from typing import Any, Dict, List, Tuple
from unittest.mock import MagicMock
from faker import Faker
from fastapi import FastAPI
from pgpy.pgp import PGPKey
from pytest_mock import MockerFixture
from responses import RequestsMock
from starlette.testclient import TestClient

from . import utils


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def enable_cors_origins_single(monkeypatch: pytest.MonkeyPatch, faker: Faker) -> str:
    origin: str = faker.url()
    monkeypatch.setenv("CORS_ORIGINS", f'["{origin}"]')
    return origin


@pytest.fixture(scope="function")
def enable_cors_origins_multiple(
    monkeypatch: pytest.MonkeyPatch, faker: Faker
) -> List[str]:
    import json

    origins: List[str] = [faker.url(), faker.url()]
    monkeypatch.setenv("CORS_ORIGINS", f"{json.dumps(origins)}")

    return origins


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def enable_smtp_ssl(monkeypatch: pytest.MonkeyPatch, faker: Faker) -> None:
    monkeypatch.setenv("SMTP_PORT", "465")
    monkeypatch.setenv("SMTP_TLS", "false")
    monkeypatch.setenv("SMTP_SSL", "true")


@pytest.fixture(scope="function")
def mock_smtp_ssl(mocker: MockerFixture) -> MagicMock:
    mock_client = mocker.patch("smtplib.SMTP_SSL", autospec=True)

    return mock_client


@pytest.fixture(scope="function")
def mock_smtp(mocker: MockerFixture) -> MagicMock:
    mock_client = mocker.patch("smtplib.SMTP", autospec=True)

    return mock_client


@pytest.fixture(scope="function")
def mock_smtp_connect_error(mock_smtp: MagicMock) -> MagicMock:
    from smtplib import SMTPConnectError

    mock_smtp.side_effect = SMTPConnectError(400, "error")

    return mock_smtp


@pytest.fixture(scope="function")
def mock_smtp_tls_error(mock_smtp: MagicMock, mocker: MockerFixture) -> MagicMock:
    from smtplib import SMTPNotSupportedError

    mock_smtp.return_value.starttls = mocker.Mock(
        side_effect=SMTPNotSupportedError(400, "error")
    )

    return mock_smtp


@pytest.fixture(scope="function")
def mock_smtp_auth_error(mock_smtp: MagicMock, mocker: MockerFixture) -> MagicMock:
    from smtplib import SMTPAuthenticationError

    mock_smtp.return_value.login = mocker.Mock(
        side_effect=SMTPAuthenticationError(401, "error")
    )

    return mock_smtp


@pytest.fixture(scope="function")
def mock_smtp_send_error(mock_smtp: MagicMock, mocker: MockerFixture) -> MagicMock:
    from smtplib import SMTPDataError

    mock_smtp.return_value.send_message = mocker.Mock(
        side_effect=SMTPDataError(402, "error")
    )

    return mock_smtp


# ------------------------------------------------------------------------------


valid_recaptcha_secret = "valid-recaptcha-secret"
valid_recaptcha_response = "valid-recaptcha-response"


@pytest.fixture(scope="function")
def enable_recaptcha(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RECAPTCHA_SECRET_KEY", valid_recaptcha_secret)


@pytest.fixture(scope="function")
def enable_recaptcha_invalid_secret(
    monkeypatch: pytest.MonkeyPatch, faker: Faker
) -> None:
    monkeypatch.setenv("RECAPTCHA_SECRET_KEY", faker.pystr())


@pytest.fixture(scope="function")
def mock_recaptcha_verify_api(responses: RequestsMock, faker: Faker) -> RequestsMock:
    from requests.models import PreparedRequest
    from mailer import recaptcha

    def request_callback(
        request: PreparedRequest,
    ) -> Tuple[HTTPStatus, Dict[str, Any], str]:
        import json
        from urllib.parse import parse_qs

        headers: Dict[str, Any] = {}

        params = parse_qs(str(request.body))
        secret = params.get("secret")
        response = params.get("response")

        errors = []
        if secret and secret != [valid_recaptcha_secret]:
            errors.append("invalid-input-secret")

        if not response:
            errors.append("missing-input-response")
        elif response != [valid_recaptcha_response]:
            errors.append("invalid-input-response")

        body: Dict[str, Any] = {}
        if len(errors) > 0:
            body["success"] = False
            body["error-codes"] = errors
        else:
            body["success"] = True
            body["challenge_ts"] = faker.iso8601()
            body["hostname"] = faker.hostname()

        return (HTTPStatus.OK, headers, json.dumps(body))

    responses.add_callback(
        responses.POST,
        recaptcha.verify_url,
        callback=request_callback,
        content_type="application/json",
    )

    return responses


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def enable_pgp_public_key(monkeypatch: pytest.MonkeyPatch, faker: Faker) -> PGPKey:
    pgp_key = utils.generate_pgp_key_pair(faker.name(), faker.email())
    pub_key = urlsafe_b64encode(str(pgp_key.pubkey).encode("utf-8")).decode("utf-8")
    monkeypatch.setenv("PGP_PUBLIC_KEY", pub_key)

    return pgp_key


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def no_success_redirect_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SUCCESS_REDIRECT_URL")


@pytest.fixture(scope="function")
def no_error_redirect_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ERROR_REDIRECT_URL")


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def params_success(faker: Faker) -> Dict[str, str]:
    return {
        "email": faker.email(),
        "name": faker.name(),
        "subject": faker.text(max_nb_chars=100),
        "message": faker.text(max_nb_chars=1000),
        "honeypot": "",
    }


# ------------------------------------------------------------------------------


def test_get_api_info_success(app_client: TestClient) -> None:
    from mailer import __about__

    response = app_client.get("/api/")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["name"] == __about__.__title__
    assert data["version"] == __about__.__version__
    assert data["api_version"] == "v1"


# ------------------------------------------------------------------------------


def test_send_mail_success(
    app: FastAPI,
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["email"] == params["email"]
    assert data["name"] == params["name"]
    assert data["subject"] == params["subject"]
    assert data["message"] == params["message"]
    assert data["honeypot"] == params["honeypot"]

    assert mock_smtp.call_count == 1
    assert mock_smtp.return_value.starttls.call_count == 1
    assert mock_smtp.return_value.login.call_count == 1
    assert mock_smtp.return_value.send_message.call_count == 1
    assert mock_smtp.return_value.quit.call_count == 1

    sent_msg = mock_smtp.return_value.send_message.call_args.args[0].as_string()
    app_settings = app.state.settings
    utils.assert_plain_email(
        sent_msg,
        params["email"],
        params["name"],
        params["subject"],
        params["message"],
        app_settings.sender_email,
        app_settings.to_email,
        app_settings.to_name,
    )


def test_send_mail_ssl_success(
    enable_smtp_ssl: None,
    app: FastAPI,
    app_client: TestClient,
    mock_smtp_ssl: MagicMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["email"] == params["email"]
    assert data["name"] == params["name"]
    assert data["subject"] == params["subject"]
    assert data["message"] == params["message"]
    assert data["honeypot"] == params["honeypot"]

    assert mock_smtp_ssl.call_count == 1

    sent_msg = mock_smtp_ssl.return_value.send_message.call_args.args[0].as_string()
    app_settings = app.state.settings
    utils.assert_plain_email(
        sent_msg,
        params["email"],
        params["name"],
        params["subject"],
        params["message"],
        app_settings.sender_email,
        app_settings.to_email,
        app_settings.to_name,
    )


def test_send_mail_smtp_connect_failed(
    app_client: TestClient,
    mock_smtp_connect_error: MagicMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    assert mock_smtp_connect_error.call_count == 1
    assert mock_smtp_connect_error.return_value.starttls.call_count == 0
    assert mock_smtp_connect_error.return_value.login.call_count == 0
    assert mock_smtp_connect_error.return_value.send_message.call_count == 0
    assert mock_smtp_connect_error.return_value.quit.call_count == 0


def test_send_mail_smtp_tls_failed(
    app_client: TestClient,
    mock_smtp_tls_error: MagicMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    assert mock_smtp_tls_error.call_count == 1
    assert mock_smtp_tls_error.return_value.starttls.call_count == 1
    assert mock_smtp_tls_error.return_value.login.call_count == 0
    assert mock_smtp_tls_error.return_value.send_message.call_count == 0
    assert mock_smtp_tls_error.return_value.quit.call_count == 0


def test_send_mail_smtp_login_failed(
    app_client: TestClient,
    mock_smtp_auth_error: MagicMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    assert mock_smtp_auth_error.call_count == 1
    assert mock_smtp_auth_error.return_value.starttls.call_count == 1
    assert mock_smtp_auth_error.return_value.login.call_count == 1
    assert mock_smtp_auth_error.return_value.send_message.call_count == 0
    assert mock_smtp_auth_error.return_value.quit.call_count == 0


def test_send_mail_smtp_send_failed(
    app_client: TestClient,
    mock_smtp_send_error: MagicMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    assert mock_smtp_send_error.call_count == 1
    assert mock_smtp_send_error.return_value.starttls.call_count == 1
    assert mock_smtp_send_error.return_value.login.call_count == 1
    assert mock_smtp_send_error.return_value.send_message.call_count == 1
    assert mock_smtp_send_error.return_value.quit.call_count == 0


def test_send_mail_none(app_client: TestClient, mock_smtp: MagicMock) -> None:
    params: Dict[str, str] = {}

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_empty_fields(app_client: TestClient, mock_smtp: MagicMock) -> None:
    params = {"email": "", "name": "", "subject": "", "message": "", "honeypot": ""}

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_empty_email(
    app_client: TestClient, mock_smtp: MagicMock, params_success: Dict[str, str]
) -> None:
    params = params_success
    params["email"] = ""

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_empty_name(
    app_client: TestClient, mock_smtp: MagicMock, params_success: Dict[str, str]
) -> None:
    params = params_success
    params["name"] = ""

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_empty_subject(
    app_client: TestClient, mock_smtp: MagicMock, params_success: Dict[str, str]
) -> None:
    params = params_success
    params["subject"] = ""

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_empty_message(
    app_client: TestClient, mock_smtp: MagicMock, params_success: Dict[str, str]
) -> None:
    params = params_success
    params["message"] = ""

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_bad_email(
    app_client: TestClient, mock_smtp: MagicMock, params_success: Dict[str, str]
) -> None:
    params = params_success
    params["email"] = "joe@doe"

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_too_long_name(
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    params = params_success
    params["name"] = faker.text(max_nb_chars=100)

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_too_long_subject(
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    params = params_success
    params["subject"] = faker.text(max_nb_chars=2000)

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_too_long_message(
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    params = params_success
    params["message"] = faker.text(max_nb_chars=2000)

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_non_empty_honeypot(
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    params = params_success
    params["honeypot"] = faker.text()

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_mail_cors_origin_single(
    enable_cors_origins_single: str,
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    params = params_success

    response = app_client.options(
        "/api/mail",
        headers={
            "Origin": enable_cors_origins_single,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.headers["access-control-allow-origin"] == enable_cors_origins_single

    response = app_client.post(
        "/api/mail", json=params, headers={"Origin": enable_cors_origins_single}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.headers["access-control-allow-origin"] == enable_cors_origins_single

    response = app_client.post(
        "/api/mail", json=params, headers={"Origin": faker.url()}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_send_mail_cors_origin_multiple(
    enable_cors_origins_multiple: List[str],
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    params = params_success

    for origin in enable_cors_origins_multiple:
        response = app_client.options(
            "/api/mail",
            headers={"Origin": origin, "Access-Control-Request-Method": "GET"},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.headers["access-control-allow-origin"] == origin

        response = app_client.post("/api/mail", json=params, headers={"Origin": origin})
        assert response.status_code == HTTPStatus.OK
        assert response.headers["access-control-allow-origin"] == origin

    response = app_client.post(
        "/api/mail", json=params, headers={"Origin": faker.url()}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_send_mail_recaptcha_success(
    enable_recaptcha: None,
    app_client: TestClient,
    mock_smtp: MagicMock,
    mock_recaptcha_verify_api: RequestsMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success
    params["g-recaptcha-response"] = valid_recaptcha_response

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.OK


def test_send_mail_recaptcha_invalid_secret(
    enable_recaptcha_invalid_secret: None,
    app_client: TestClient,
    mock_smtp: MagicMock,
    mock_recaptcha_verify_api: RequestsMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success
    params["g-recaptcha-response"] = valid_recaptcha_response

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_send_mail_recaptcha_no_response(
    enable_recaptcha: None,
    app_client: TestClient,
    mock_smtp: MagicMock,
    mock_recaptcha_verify_api: RequestsMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success
    params["g-recaptcha-response"] = ""

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_send_mail_recaptcha_invalid_response(
    enable_recaptcha: None,
    app_client: TestClient,
    mock_smtp: MagicMock,
    mock_recaptcha_verify_api: RequestsMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    params = params_success
    params["g-recaptcha-response"] = faker.pystr()

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_send_pgp_mail_success(
    enable_pgp_public_key: PGPKey,
    app: FastAPI,
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["email"] == params["email"]
    assert data["name"] == params["name"]
    assert data["subject"] == params["subject"]
    assert data["message"] == params["message"]
    assert data["honeypot"] == params["honeypot"]

    assert mock_smtp.call_count == 1
    assert mock_smtp.return_value.login.call_count == 1
    assert mock_smtp.return_value.send_message.call_count == 1
    assert mock_smtp.return_value.quit.call_count == 1

    message = mock_smtp.return_value.send_message.call_args.args[0]
    sent_msg = message.as_string()
    app_settings = app.state.settings
    embedded_pub_key = utils.assert_pgp_email(
        sent_msg,
        params["email"],
        params["name"],
        params["subject"],
        params["message"],
        app_settings.sender_email,
        app_settings.to_email,
        app_settings.to_name,
        enable_pgp_public_key,
        None,
    )
    assert embedded_pub_key is None


def test_send_pgp_mail_with_attached_public_key_success(
    enable_pgp_public_key: PGPKey,
    app: FastAPI,
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    sender_key = utils.generate_pgp_key_pair(faker.name(), faker.email())

    params = params_success
    params["public_key"] = str(sender_key.pubkey)

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["email"] == params["email"]
    assert data["name"] == params["name"]
    assert data["subject"] == params["subject"]
    assert data["message"] == params["message"]
    assert data["honeypot"] == params["honeypot"]

    assert mock_smtp.call_count == 1
    assert mock_smtp.return_value.login.call_count == 1
    assert mock_smtp.return_value.send_message.call_count == 1
    assert mock_smtp.return_value.quit.call_count == 1

    message = mock_smtp.return_value.send_message.call_args.args[0]
    sent_msg = message.as_string()
    app_settings = app.state.settings
    embedded_pub_key = utils.assert_pgp_email(
        sent_msg,
        params["email"],
        params["name"],
        params["subject"],
        params["message"],
        app_settings.sender_email,
        app_settings.to_email,
        app_settings.to_name,
        enable_pgp_public_key,
        sender_key.pubkey,
    )
    assert embedded_pub_key == str(sender_key.pubkey)

    email_response = faker.text()
    pgp_response = utils.encrypt_pgp_message(embedded_pub_key, email_response)
    plain_response = utils.decrypt_pgp_message(str(sender_key), pgp_response)
    assert plain_response == email_response


def test_send_pgp_mail_with_attached_public_key_private(
    enable_pgp_public_key: PGPKey,
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    sender_key = utils.generate_pgp_key_pair(faker.name(), faker.email())

    params = params_success
    params["public_key"] = str(sender_key)

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_send_pgp_mail_with_attached_public_key_invalid(
    enable_pgp_public_key: PGPKey,
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    pgp_key = urlsafe_b64encode(faker.binary()).decode("utf-8")

    params = params_success
    params["public_key"] = pgp_key

    response = app_client.post("/api/mail", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# ------------------------------------------------------------------------------


def test_send_mail_form_success(
    app: FastAPI,
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success

    response = app_client.post("/api/mail/form", data=params, follow_redirects=False)
    assert response.status_code == HTTPStatus.FOUND
    assert response.headers["Location"] == os.environ["SUCCESS_REDIRECT_URL"]

    assert mock_smtp.call_count == 1
    assert mock_smtp.return_value.starttls.call_count == 1
    assert mock_smtp.return_value.login.call_count == 1
    assert mock_smtp.return_value.send_message.call_count == 1
    assert mock_smtp.return_value.quit.call_count == 1

    sent_msg = mock_smtp.return_value.send_message.call_args.args[0].as_string()
    app_settings = app.state.settings
    utils.assert_plain_email(
        sent_msg,
        params["email"],
        params["name"],
        params["subject"],
        params["message"],
        app_settings.sender_email,
        app_settings.to_email,
        app_settings.to_name,
    )


def test_send_mail_form_redirect_origin(
    no_success_redirect_url: None,
    app: FastAPI,
    app_client: TestClient,
    mock_smtp: MagicMock,
    params_success: Dict[str, str],
    faker: Faker,
) -> None:
    origin = faker.url()
    params = params_success

    response = app_client.post(
        "/api/mail/form",
        headers={"Origin": origin},
        data=params,
        follow_redirects=False,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.headers["Location"] == origin

    assert mock_smtp.call_count == 1
    assert mock_smtp.return_value.starttls.call_count == 1
    assert mock_smtp.return_value.login.call_count == 1
    assert mock_smtp.return_value.send_message.call_count == 1
    assert mock_smtp.return_value.quit.call_count == 1


def test_send_mail_form_none(app_client: TestClient) -> None:
    params: Dict[str, str] = {}

    response = app_client.post("/api/mail/form", data=params, follow_redirects=False)
    assert response.status_code == HTTPStatus.FOUND
    assert response.headers["Location"] == os.environ["ERROR_REDIRECT_URL"]


def test_send_mail_form_none_redirect_origin(
    no_error_redirect_url: None,
    app_client: TestClient,
    faker: Faker,
) -> None:
    origin = faker.url()

    params: Dict[str, str] = {}

    response = app_client.post(
        "/api/mail/form",
        headers={"Origin": origin},
        data=params,
        follow_redirects=False,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.headers["Location"] == origin


def test_send_mail_form_recaptcha_invalid_secret(
    enable_recaptcha_invalid_secret: None,
    app_client: TestClient,
    mock_smtp: MagicMock,
    mock_recaptcha_verify_api: RequestsMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success
    params["g-recaptcha-response"] = valid_recaptcha_response

    response = app_client.post("/api/mail/form", data=params, follow_redirects=False)
    assert response.status_code == HTTPStatus.FOUND
    assert response.headers["Location"] == os.environ["ERROR_REDIRECT_URL"]


def test_send_mail_form_smtp_send_failed(
    app_client: TestClient,
    mock_smtp_send_error: MagicMock,
    params_success: Dict[str, str],
) -> None:
    params = params_success

    response = app_client.post("/api/mail/form", data=params, follow_redirects=False)
    assert response.status_code == HTTPStatus.FOUND
    assert response.headers["Location"] == os.environ["ERROR_REDIRECT_URL"]

    assert mock_smtp_send_error.call_count == 1
    assert mock_smtp_send_error.return_value.starttls.call_count == 1
    assert mock_smtp_send_error.return_value.login.call_count == 1
    assert mock_smtp_send_error.return_value.send_message.call_count == 1
    assert mock_smtp_send_error.return_value.quit.call_count == 0
