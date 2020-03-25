from typing import Optional, Set
from pydantic import BaseSettings, EmailStr, AnyHttpUrl

from . import __about__


class Settings(BaseSettings):
    app_version: str = __about__.__version__
    app_environment: str = "production"

    sender_email: EmailStr
    to_email: EmailStr
    to_name: str

    mailer_provider: str = "sendgrid"

    sendgrid_api_key: Optional[str] = None
    sendgrid_sandbox: bool = False

    cors_origins: Set[AnyHttpUrl] = set()

    recaptcha_secret_key: Optional[str]

    sentry_dsn: Optional[str] = None
