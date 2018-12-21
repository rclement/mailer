import sendgrid
import python_http_client

from sendgrid.helpers.mail import (
    Content,
    Email,
    Mail,
    MailSettings,
    SandBoxMode,
    SpamCheck,
)


# ------------------------------------------------------------------------------


class SendgridMailer:
    def __init__(self, api_key, sandbox=False):
        self.sg = sendgrid.SendGridAPIClient(apikey=api_key)
        self.sandbox = sandbox

    def send_mail(self, from_email, from_name, to_email, to_name, subject, message):
        mail_settings = MailSettings()
        mail_settings.sandbox_mode = SandBoxMode(self.sandbox)
        mail_settings.spam_check = SpamCheck(
            True, 1, "https://spamcatcher.sendgrid.com"
        )

        from_email = Email(email=from_email, name=from_name)
        to_email = Email(email=to_email, name=to_name)
        content = Content("text/plain", message)
        mail = Mail(from_email, subject, to_email, content)
        mail.mail_settings = mail_settings

        try:
            rv = self.sg.client.mail.send.post(request_body=mail.get())
        except python_http_client.exceptions.HTTPError as e:
            rv = e

        return rv
