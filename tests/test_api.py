from http import HTTPStatus
from python_http_client import exceptions as phce
from .utils import JsonRequest


routes = {"index": "/api/", "mail": "/api/mail"}


def _post_mail_accepted(client, mocker, params):
    status_code = HTTPStatus.ACCEPTED

    mock = mocker.Mock()
    mock.getcode.return_value = status_code
    mock.read.return_value = ""
    mock.info.return_value = ""

    mock_client = mocker.patch("python_http_client.Client._make_request")
    mock_client.return_value = mock

    rq = JsonRequest(params)
    rv = client.post(routes["mail"], data=rq.json, content_type=rq.content_type)

    assert rv.status_code == status_code
    assert rv.json == params


def _post_mail_unauthorized(client, mocker, params):
    status_code = HTTPStatus.UNAUTHORIZED

    mock = mocker.Mock()
    mock.code = status_code
    mock.reason = ""
    mock.hdrs = ""
    mock.read.return_value = ""

    mock_client = mocker.patch("python_http_client.Client._make_request")
    mock_client.side_effect = phce.UnauthorizedError(mock)

    rq = JsonRequest(params)
    rv = client.post(routes["mail"], data=rq.json, content_type=rq.content_type)

    assert rv.status_code == status_code


def _post_mail_error(client, params):
    rq = JsonRequest(params)
    rv = client.post(routes["mail"], data=rq.json, content_type=rq.content_type)

    assert rv.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_index(client):
    rv = client.get(routes["index"])

    assert rv.status_code == HTTPStatus.OK
    assert rv.json == {"version": "v1"}


def test_post_mail_accepted(client, mocker):
    params = {
        "email": "john@doe.com",
        "name": "John Doe",
        "subject": "Test",
        "message": "Hi there!",
        "honeypot": "",
    }

    _post_mail_accepted(client, mocker, params)


def test_post_mail_unauthorized(client, mocker):
    params = {
        "email": "john@doe.com",
        "name": "John Doe",
        "subject": "Test",
        "message": "Hi there!",
        "honeypot": "",
    }

    _post_mail_unauthorized(client, mocker, params)


def test_post_mail_none(client):
    params = {}
    _post_mail_error(client, params)


def test_post_mail_empty_all(client):
    params = {"email": "", "name": "", "subject": "", "message": "", "honeypot": ""}
    _post_mail_error(client, params)


def test_post_mail_empty_name(client):
    params = {
        "email": "john@doe.com",
        "name": "",
        "subject": "Test",
        "message": "Hi there!",
    }
    _post_mail_error(client, params)


def test_post_mail_empty_subject(client):
    params = {
        "email": "john@doe.com",
        "name": "John Doe",
        "subject": "",
        "message": "Hi there!",
    }
    _post_mail_error(client, params)


def test_post_mail_empty_message(client):
    params = {
        "email": "john@doe.com",
        "name": "John Doe",
        "subject": "Test",
        "message": "",
    }
    _post_mail_error(client, params)


def test_post_mail_bad_email(client):
    params = {"email": "john@", "name": "John Doe", "subject": "Test", "message": ""}
    _post_mail_error(client, params)


def test_post_mail_too_long_email(client):
    params = {
        "email": "johnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohn@doe.com",
        "name": "John Doe",
        "subject": "Test",
        "message": "Hi there!",
    }
    _post_mail_error(client, params)


def test_post_mail_too_long_name(client):
    params = {
        "email": "john@doe.com",
        "name": "JohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohn Doe",
        "subject": "Test",
        "message": "Hi there!",
    }
    _post_mail_error(client, params)


def test_post_mail_too_long_subject(client):
    params = {
        "email": "john@doe.com",
        "name": "John Doe",
        "subject": "Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test ",
        "message": "Hi there!",
    }
    _post_mail_error(client, params)


def test_post_mail_too_long_message(client):
    params = {
        "email": "john@doe.com",
        "name": "John Doe",
        "subject": "Test",
        "message": "Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! Hi there! ",
    }
    _post_mail_error(client, params)


def test_post_mail_non_empty_honeypot(client):
    params = {
        "email": "john@doe.com",
        "name": "John Doe",
        "subject": "Test",
        "message": "Hi there!",
        "honeypot": "abcdefghijklmnopqrs",
    }
    _post_mail_error(client, params)
