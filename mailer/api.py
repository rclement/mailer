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
    email: EmailStr = Field(
        ...,
        title="E-mail",
        description="E-mail address of the contact sending the message",
    )
    name: str = Field(
        ...,
        title="Name",
        description="Name of the contact sending the message",
        min_length=1,
        max_length=50,
    )
    subject: str = Field(
        ...,
        title="Subject",
        description="Subject of the message to be sent",
        min_length=1,
        max_length=100,
    )
    message: str = Field(
        ...,
        title="Message",
        description="Content of the message to be sent",
        min_length=1,
        max_length=200,
    )
    honeypot: str = Field(
        ...,
        title="Honeypot",
        description="Spam-bot filtering honeypot: if your are not a bot, just send an empty string!",
        min_length=0,
        max_length=0,
    )
    g_recaptcha_response: Optional[str] = Field(
        None,
        alias="g-recaptcha-response",
        title="Google ReCaptcha Response",
        description="Obtained response from Google ReCaptcha v2 widget (or invisible)",
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
