from typing import Optional, Set
from pydantic import BaseSettings, EmailStr, AnyHttpUrl

from . import __about__


class Settings(BaseSettings):
    app_title: str = __about__.__title__
    app_description: str = __about__.__description__
    app_version: str = __about__.__version__
    app_environment: str = "production"

    sender_email: EmailStr
    to_email: EmailStr
    to_name: str

    smtp_host: str
    smtp_port: int
    smtp_tls: bool
    smtp_ssl: bool
    smtp_user: str
    smtp_password: str

    cors_origins: Set[AnyHttpUrl] = set()

    recaptcha_secret_key: Optional[str]

    sentry_dsn: Optional[str] = None
