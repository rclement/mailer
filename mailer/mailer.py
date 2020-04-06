import dataclasses
import smtplib

from email import encoders
from email.header import Header
from email.message import EmailMessage, Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate
from typing import Any, Dict, Optional
from pgpy import PGPKey, PGPMessage
from pgpy.errors import PGPError


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
    pgp_public_key: Optional[PGPKey]

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
        self,
        from_email: str,
        from_name: str,
        subject: str,
        message: str,
        public_key: Optional[str],
    ) -> None:
        if self.pgp_public_key:
            return self._send_encrypted_email(
                from_email, from_name, subject, message, public_key, self.pgp_public_key
            )
        else:
            return self._send_plain_email(from_email, from_name, subject, message)

    def _send_plain_email(
        self, from_email: str, from_name: str, subject: str, message: str
    ) -> None:
        msg = MIMEMultipart("mixed")
        msg["Date"] = formatdate()
        msg["From"] = formataddr((from_name, self.sender_email))
        msg["To"] = formataddr((self.to_name, self.to_email))
        msg["Reply-To"] = formataddr((from_name, from_email))
        msg["Subject"] = Header(subject, "utf-8")
        msg.preamble = "This is a multi-part message in MIME format.\n"

        msg_text = MIMEText(message, _subtype="plain", _charset="utf-8")
        msg.attach(msg_text)

        self._send_smtp(msg)

    def _send_encrypted_email(
        self,
        from_email: str,
        from_name: str,
        subject: str,
        message: str,
        public_key: Optional[str],
        pgp_public_key: PGPKey,
    ) -> None:
        # Sources:
        # - [ProtonMail](https://protonmail.com/support/knowledge-base/pgp-mime-pgp-inline/)
        # - [StackOverflow](https://stackoverflow.com/questions/54486279/how-to-send-gpg-encrypted-email-with-attachment-using-python?answertab=active#tab-top)

        msg = EmailMessage()
        msg.add_header(_name="Content-Type", _value="multipart/mixed")

        msg_text = MIMEText(message, _subtype="plain", _charset="utf-8")
        msg.attach(msg_text)

        if public_key:
            msg_attachment = EmailMessage()
            msg_attachment.add_header(
                _name="Content-Type",
                _value="application/pgp-keys",
                name="publickey.asc",
            )
            msg_attachment.add_header(
                _name="Content-Disposition",
                _value="attachment",
                filename="publickey.asc",
            )
            msg_attachment.set_payload(public_key)
            encoders.encode_base64(msg_attachment)
            msg.attach(msg_attachment)

        try:
            encrypted_message = pgp_public_key.encrypt(PGPMessage.new(msg.as_string()))
        except PGPError:
            raise RuntimeError

        pgp_msg = MIMEBase(
            _maintype="multipart",
            _subtype="encrypted",
            protocol="application/pgp-encrypted",
            charset="UTF-8",
        )

        pgp_msg["Date"] = formatdate()
        pgp_msg["From"] = formataddr((from_name, self.sender_email))
        pgp_msg["To"] = formataddr((self.to_name, self.to_email))
        pgp_msg["Reply-To"] = formataddr((from_name, from_email))
        pgp_msg["Subject"] = Header(subject, "utf-8")

        pgp_msg_part1 = EmailMessage()
        pgp_msg_part1.add_header(
            _name="Content-Type", _value="application/pgp-encrypted"
        )
        pgp_msg_part1.add_header(
            _name="Content-Description", _value="PGP/MIME version identification"
        )
        pgp_msg_part1.set_payload("Version: 1\n")
        pgp_msg.attach(pgp_msg_part1)

        pgp_msg_part2 = EmailMessage()
        pgp_msg_part2.add_header(
            _name="Content-Type",
            _value="application/octet-stream",
            name="encrypted.asc",
        )
        pgp_msg_part2.add_header(
            _name="Content-Description", _value="OpenPGP encrypted message"
        )
        pgp_msg_part2.add_header(
            _name="Content-Disposition", _value="inline", filename="encrypted.asc"
        )
        pgp_msg_part2.set_payload(str(encrypted_message))
        pgp_msg.attach(pgp_msg_part2)

        return self._send_smtp(pgp_msg)

    def _send_smtp(self, message: Message) -> None:
        try:
            s = smtplib.SMTP(
                host=self.smtp_config["host"], port=self.smtp_config["port"]
            )
            s.login(
                user=self.smtp_config["user"], password=self.smtp_config["password"]
            )
            s.send_message(message)
            s.quit()
        except smtplib.SMTPResponseException:
            raise RuntimeError
