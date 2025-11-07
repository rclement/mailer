from pydantic import EmailStr, AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pgpy import PGPKey

from . import __about__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    app_title: str = __about__.__title__
    app_description: str = __about__.__description__
    app_version: str = __about__.__version__
    app_environment: str = "production"

    sender_email: EmailStr
    to_email: EmailStr
    to_name: str
    success_redirect_url: AnyHttpUrl | None = None
    error_redirect_url: AnyHttpUrl | None = None

    smtp_host: str
    smtp_port: int
    smtp_tls: bool
    smtp_ssl: bool
    smtp_user: str
    smtp_password: str

    pgp_public_key: PGPKey | None = None

    force_https: bool = True
    cors_origins: set[AnyHttpUrl] = set()

    recaptcha_secret_key: str | None = None

    sentry_dsn: str | None = None

    @field_validator("pgp_public_key", mode="before")
    @classmethod
    def validate_pgp_public_key(cls, v: str | None) -> PGPKey | None:
        from base64 import urlsafe_b64decode
        from pgpy.errors import PGPError

        if v:
            try:
                public_key_str = urlsafe_b64decode(v)
                key, _ = PGPKey.from_blob(public_key_str)
            except (ValueError, PGPError):
                raise ValueError("Invalid PGP public key: cannot load the key")

            if not key.is_public:
                raise ValueError("Invalid PGP public key: key is private")

            return key

        return None
