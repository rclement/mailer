from http import HTTPStatus
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator

from . import recaptcha
from .mailer import Mailer
from .settings import Settings


router = APIRouter()


class ApiInfoSchema(BaseModel):
    name: str = Field(..., title="Name", description="Name of the app")
    version: str = Field(..., title="Version", description="Version of the app")
    api_version: str = Field(..., title="API Version", description="Version of the API")


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
        max_length=1000,
    )
    honeypot: str = Field(
        ...,
        title="Honeypot",
        description="Spam-bot filtering honeypot: if your are not a bot, just send an empty string!",
        min_length=0,
        max_length=0,
    )
    g_recaptcha_response: str | None = Field(
        None,
        alias="g-recaptcha-response",
        title="Google ReCaptcha Response",
        description="Obtained response from Google ReCaptcha v2 widget (or invisible)",
    )
    public_key: str | None = Field(
        None,
        title="PGP public key",
        description="ASCII-armored PGP public of the contact sending the message, to be attached within the e-mail",
        validate_default=True,
    )

    @field_validator("public_key")
    @classmethod
    def validate_public_key(cls, v: str | None) -> str | None:
        from pgpy import PGPKey
        from pgpy.errors import PGPError

        if v:
            try:
                key, _ = PGPKey.from_blob(v.encode("utf-8"))
            except (ValueError, PGPError):
                raise ValueError("Invalid PGP public key: cannot load the key")

            if not key.is_public:
                raise ValueError("Invalid PGP public key: key is private")

        return v


def check_origin(req: Request, origin: str = Header(None)) -> None:
    settings: Settings = req.app.state.settings
    if len(settings.cors_origins) > 0:
        if origin.rstrip("/") not in settings.cors_origins_list:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized origin")


@router.get(
    "/",
    summary="Information",
    description="Obtain API information",
    response_model=ApiInfoSchema,
)
def get_api_info(req: Request) -> dict[str, str]:
    settings: Settings = req.app.state.settings
    data = {
        "name": settings.app_title,
        "version": settings.app_version,
        "api_version": "v1",
    }

    return data


@router.post(
    "/mail",
    summary="Send e-mail",
    description="Send an e-mail from a contact",
    dependencies=[Depends(check_origin)],
    response_model=MailSchema,
    responses={
        str(int(HTTPStatus.UNAUTHORIZED)): {"description": "Unauthorized operation"}
    },
)
def post_mail(req: Request, mail: MailSchema) -> MailSchema:
    settings: Settings = req.app.state.settings

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
        settings.pgp_public_key,
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
            public_key=mail.public_key,
        )
    except RuntimeError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED)

    return mail


@router.post(
    "/mail/form",
    summary="Send e-mail (url-encoded form)",
    description="Send an e-mail from an URL-encoded contact form",
    dependencies=[Depends(check_origin)],
    responses={
        str(int(HTTPStatus.UNAUTHORIZED)): {"description": "Unauthorized operation"}
    },
)
async def post_mail_form(req: Request) -> RedirectResponse:
    settings: Settings = req.app.state.settings

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
        settings.pgp_public_key,
    )

    try:
        form = await req.form()
        mail = MailSchema(**form)

        recaptcha.verify(
            secret_key=settings.recaptcha_secret_key, response=mail.g_recaptcha_response
        )

        mailer.send_email(
            from_email=mail.email,
            from_name=mail.name,
            subject=mail.subject,
            message=mail.message,
            public_key=mail.public_key,
        )
    except (ValidationError, RuntimeError):
        return RedirectResponse(
            settings.error_redirect_url or req.headers["Origin"],
            status_code=HTTPStatus.FOUND,
        )

    return RedirectResponse(
        settings.success_redirect_url or req.headers["Origin"],
        status_code=HTTPStatus.FOUND,
    )
