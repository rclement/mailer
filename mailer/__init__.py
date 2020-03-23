from fastapi import FastAPI


def create_app() -> FastAPI:
    from fastapi.middleware.cors import CORSMiddleware
    from . import __about__, api, sentry
    from .settings import Settings

    settings = Settings()

    app = FastAPI(
        title=__about__.__title__,
        description=__about__.__description__,
        version=__about__.__version__,
    )
    app.settings = settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api.router, prefix="/api", tags=["api"])

    sentry.init(app)

    return app


app = create_app()
