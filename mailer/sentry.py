import sentry_sdk

from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware


def init(app: FastAPI) -> None:
    sentry_sdk.init(
        dsn=app.settings.sentry_dsn,
        environment=app.settings.app_environment,
        release=app.settings.app_version,
    )

    app.add_middleware(SentryAsgiMiddleware)
