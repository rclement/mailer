from typing import Optional, Set
from pydantic import BaseSettings, EmailStr, AnyHttpUrl, validator
from pgpy import PGPKey

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

    pgp_public_key: Optional[PGPKey] = None

    force_https: bool = True
    cors_origins: Set[AnyHttpUrl] = set()

    recaptcha_secret_key: Optional[str]

    sentry_dsn: Optional[str] = None

    @validator("pgp_public_key", pre=True)
    def validate_pgp_public_key(cls, v: Optional[str]) -> Optional[PGPKey]:
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
