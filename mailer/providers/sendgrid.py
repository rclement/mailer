import sendgrid
import python_http_client

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
    def __init__(self, api_key, sandbox=False):
        self.sg = sendgrid.SendGridAPIClient(api_key=api_key)
        self.sandbox = sandbox

    def send_mail(
        self, from_email, from_name, sender_email, to_email, to_name, subject, message
    ):
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
