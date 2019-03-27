from flask_apispec.extension import FlaskApiSpec
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr
from flask_recaptcha import ReCaptcha
from flask_talisman import Talisman


# ------------------------------------------------------------------------------


class Mailer:
    def __init__(self):
        self.to_email = None
        self.to_name = None
        self.client = None

    def init_app(self, app):
        services = {"sendgrid": self._init_sendgrid}

        self.to_email = app.config.get("TO_EMAIL")
        self.to_name = app.config.get("TO_NAME")

        mailer_service = app.config.get("MAILER_SERVICE")
        if mailer_service is not None and mailer_service in services.keys():
            service = services.get(mailer_service)
            self.client = service(app)

    def send_mail(self, from_email, from_name, subject, message):
        from flask import abort
        from http import HTTPStatus

        rv = self.client.send_mail(
            from_email, from_name, self.to_email, self.to_name, subject, message
        )
        if rv.status_code >= HTTPStatus.BAD_REQUEST:
            abort(rv.status_code)

    @staticmethod
    def _init_sendgrid(app):
        from .services import sendgrid

        api_key = app.config.get("SENDGRID_API_KEY")
        sandbox = app.config.get("SENDGRID_SANDBOX")
        return sendgrid.SendgridMailer(api_key, sandbox)


# ------------------------------------------------------------------------------


class Security:
    def __init__(self):
        self.talisman = Talisman()

    def init_app(self, app):
        force_https = app.config.get("PREFERRED_URL_SCHEME", "https") == "https"
        csp_policy = {}
        self.talisman.init_app(
            app=app, force_https=force_https, content_security_policy=csp_policy
        )


# ------------------------------------------------------------------------------


docs = FlaskApiSpec()
cors = CORS()
limiter = Limiter(key_func=get_ipaddr)
mailer = Mailer()
recaptcha = ReCaptcha()
security = Security()
