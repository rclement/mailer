from typing import Optional
from fastapi import FastAPI


def create_app(env_file: Optional[str] = ".env") -> FastAPI:
    from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
    from fastapi.middleware.cors import CORSMiddleware
    from . import api, home, sentry
    from .settings import Settings

    settings = Settings(_env_file=env_file)  # type: ignore

    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
        docs_url=None if settings.app_environment == "production" else "/docs",
    )
    app.state.settings = settings

    if settings.force_https:
        app.add_middleware(HTTPSRedirectMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(home.router, prefix="", tags=["home"])
    app.include_router(api.router, prefix="/api", tags=["api"])

    sentry.init(app)

    return app


app = create_app()
