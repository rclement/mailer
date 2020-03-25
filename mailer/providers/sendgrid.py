import sendgrid
import python_http_client

from typing import Any
from sendgrid.helpers.mail import (
    Content,
    From,
    Mail,
    MailSettings,
    ReplyTo,
    SandBoxMode,
    SpamCheck,
    To,
)


# ------------------------------------------------------------------------------


class SendgridMailer:
    def __init__(self, api_key: str, sandbox: bool = False):
        self.sg = sendgrid.SendGridAPIClient(api_key=api_key)
        self.sandbox = sandbox

    def send_mail(
        self,
        from_email: str,
        from_name: str,
        sender_email: str,
        to_email: str,
        to_name: str,
        subject: str,
        message: str,
    ) -> Any:
        mail_settings = MailSettings()
        mail_settings.sandbox_mode = SandBoxMode(self.sandbox)
        mail_settings.spam_check = SpamCheck(
            True, 1, "https://spamcatcher.sendgrid.com"
        )

        mail = Mail(
            from_email=From(email=sender_email, name=from_name),
            to_emails=[To(email=to_email, name=to_name)],
            subject=subject,
            plain_text_content=Content("text/plain", message),
        )
        mail.reply_to = ReplyTo(email=from_email, name=from_name)
        mail.mail_settings = mail_settings

        try:
            rv = self.sg.client.mail.send.post(request_body=mail.get())
        except python_http_client.exceptions.HTTPError as e:
            rv = e

        return rv
