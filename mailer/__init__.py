def _get_app_config(config_name):
    from .config import get_app_config

    return get_app_config(config_name)


def _init_extensions(app):
    from .extensions import cors, limiter, mailer, security

    cors.init_app(app)
    limiter.init_app(app)
    mailer.init_app(app)
    security.init_app(app)


def _register_blueprints(app):
    from .api import bp as api_bp

    blueprints = [api_bp]

    for b in blueprints:
        app.register_blueprint(b)


def _register_error_handlers(app):
    from flask import jsonify
    from http import HTTPStatus

    def error_json(error):
        data = jsonify(
            {"error": error.code, "name": error.name, "description": error.description}
        )
        data.status_code = error.code
        return data

    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    @app.errorhandler(HTTPStatus.UNAUTHORIZED)
    @app.errorhandler(HTTPStatus.FORBIDDEN)
    @app.errorhandler(HTTPStatus.NOT_FOUND)
    @app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
    @app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
    @app.errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def error_handler(error):
        return error_json(error)


def _register_cli_commands(app):
    import base64
    import secrets

    @app.cli.command()
    def generate_secret_key():
        key = base64.urlsafe_b64encode(secrets.token_bytes(128)).decode("utf-8")
        print(key)


def create_app(config_name="default"):
    from flask import Flask
    from werkzeug.contrib.fixers import ProxyFix
    from . import __about__

    app_config = _get_app_config(config_name)

    app = Flask(__about__.__title__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(app_config)

    _init_extensions(app)
    _register_blueprints(app)
    _register_error_handlers(app)
    _register_cli_commands(app)

    return app
