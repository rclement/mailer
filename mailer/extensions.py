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

        self.sender_email = app.config.get("SENDER_EMAIL")
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
            from_email,
            from_name,
            self.sender_email,
            self.to_email,
            self.to_name,
            subject,
            message,
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
        csp_policy = {}
        self.talisman.init_app(app=app, content_security_policy=csp_policy)


# ------------------------------------------------------------------------------


class Sentry:
    def init_app(self, app):
        import sentry_sdk

        from sentry_sdk.integrations.flask import FlaskIntegration
        from . import __about__

        sentry_enabled = app.config.get("SENTRY_ENABLED", False)
        sentry_dsn = app.config.get("SENTRY_DSN", None)
        sentry_environment = app.config.get("ENV", "production")
        sentry_release = __about__.__version__

        if sentry_enabled and sentry_dsn is not None:
            sentry_sdk.init(
                dsn=sentry_dsn,
                environment=sentry_environment,
                release=sentry_release,
                integrations=[FlaskIntegration()],
            )


# ------------------------------------------------------------------------------


docs = FlaskApiSpec()
cors = CORS()
limiter = Limiter(key_func=get_ipaddr)
mailer = Mailer()
recaptcha = ReCaptcha()
security = Security()
sentry = Sentry()
