from typing import Dict, Union, cast

from . import sendgrid


class Mailer:
    def __init__(
        self,
        sender_email: str,
        to_email: str,
        to_name: str,
        provider: str,
        provider_options: Dict[str, Union[bool, str, None]],
    ):
        providers = {"sendgrid": self._init_sendgrid}

        self.sender_email = sender_email
        self.to_email = to_email
        self.to_name = to_name
        self.client = None

        if provider is not None and provider in providers.keys():
            provider_func = providers[provider]
            self.client = provider_func(provider_options)

    def send_mail(
        self, from_email: str, from_name: str, subject: str, message: str
    ) -> None:
        from http import HTTPStatus

        if self.client is not None:
            rv = self.client.send_mail(
                from_email,
                from_name,
                self.sender_email,
                self.to_email,
                self.to_name,
                subject,
                message,
            )
            if rv.status_code >= HTTPStatus.BAD_REQUEST:
                raise RuntimeError(rv.status_code)

    @staticmethod
    def _init_sendgrid(
        options: Dict[str, Union[bool, str, None]]
    ) -> sendgrid.SendgridMailer:
        api_key: str = cast(str, options.get("sendgrid_api_key"))
        sandbox: bool = cast(bool, options.get("sendgrid_sandbox"))
        return sendgrid.SendgridMailer(api_key, sandbox)
