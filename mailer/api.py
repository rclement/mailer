from typing import Dict, Optional
from http import HTTPStatus
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field, validator

from . import recaptcha
from .mailer import Mailer
from .settings import Settings


router = APIRouter()


class ApiInfoSchema(BaseModel):
    name: str
    version: str
    api_version: str


class MailSchema(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=50)
    subject: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=200)
    honeypot: str
    g_recaptcha_response: Optional[str] = Field(
        None, alias="g-recaptcha-response", title="Google ReCaptcha v2 Response"
    )

    @validator("honeypot")
    def honeypot_empty(cls, v: str) -> str:
        if v != "":
            raise ValueError("Honeypot is not empty")
        return v


def check_origin(req: Request, origin: str = Header(None)) -> None:
    settings: Settings = req.app.settings
    if len(settings.cors_origins) > 0:
        if origin not in settings.cors_origins:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized origin")


@router.get("/", response_model=ApiInfoSchema)
def get_api_info(req: Request) -> Dict[str, str]:
    settings: Settings = req.app.settings
    data = {
        "name": settings.app_title,
        "version": settings.app_version,
        "api_version": "v1",
    }

    return data


@router.post(
    "/mail",
    dependencies=[Depends(check_origin)],
    response_model=MailSchema,
    responses={
        str(int(HTTPStatus.UNAUTHORIZED)): {"description": "Unauthorized operation"}
    },
)
def post_mail(req: Request, mail: MailSchema) -> MailSchema:
    settings: Settings = req.app.settings

    mailer = Mailer(
        settings.sender_email,
        settings.to_email,
        settings.to_name,
        settings.smtp_host,
        settings.smtp_port,
        settings.smtp_tls,
        settings.smtp_ssl,
        settings.smtp_user,
        settings.smtp_password,
    )

    try:
        recaptcha.verify(
            secret_key=settings.recaptcha_secret_key, response=mail.g_recaptcha_response
        )

        mailer.send_email(
            from_email=mail.email,
            from_name=mail.name,
            subject=mail.subject,
            message=mail.message,
        )
    except RuntimeError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED)

    return mail
