import sentry_sdk

from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from .settings import Settings


def init(app: FastAPI) -> None:
    settings: Settings = app.state.settings
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.app_environment,
        release=settings.app_version,
    )

    app.add_middleware(SentryAsgiMiddleware)
