from fastapi import FastAPI


def create_app() -> FastAPI:
    from fastapi.middleware.cors import CORSMiddleware
    from . import api, home, sentry
    from .settings import Settings

    settings = Settings()

    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
    )
    app.settings = settings

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
