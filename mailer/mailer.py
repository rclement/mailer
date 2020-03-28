import dataclasses
import emails

from typing import Any, Dict


@dataclasses.dataclass
class Mailer:
    sender_email: str
    to_email: str
    to_name: str
    smtp_host: dataclasses.InitVar[str]
    smtp_port: dataclasses.InitVar[int]
    smtp_tls: dataclasses.InitVar[bool]
    smtp_ssl: dataclasses.InitVar[bool]
    smtp_user: dataclasses.InitVar[str]
    smtp_password: dataclasses.InitVar[str]
    smtp_config: Dict[str, Any] = dataclasses.field(init=False)

    def __post_init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_tls: bool,
        smtp_ssl: bool,
        smtp_user: str,
        smtp_password: str,
    ) -> None:
        self.smtp_config = dict(
            host=smtp_host,
            port=smtp_port,
            tls=smtp_tls,
            ssl=smtp_ssl,
            user=smtp_user,
            password=smtp_password,
        )

    def send_email(
        self, from_email: str, from_name: str, subject: str, message: str
    ) -> None:
        msg = emails.Message(
            mail_from=(from_name, self.sender_email),
            mail_to=(self.to_name, self.to_email),
            subject=subject,
            text=message,
            headers={"Reply-To": from_email},
        )

        res = msg.send(smtp=self.smtp_config)
        if res.status_code != 250:
            raise RuntimeError
