import pgpy

from base64 import b64decode
from email import parser
from typing import Optional, Any, cast
from pgpy.constants import (
    PubKeyAlgorithm,
    KeyFlags,
    HashAlgorithm,
    SymmetricKeyAlgorithm,
    CompressionAlgorithm,
)


def generate_pgp_key_pair(name: str, email: str) -> pgpy.PGPKey:
    key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 2048)
    uid = pgpy.PGPUID.new(name, email=email)
    key.add_uid(
        uid,
        usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
        hashes=[
            HashAlgorithm.SHA256,
            HashAlgorithm.SHA384,
            HashAlgorithm.SHA512,
            HashAlgorithm.SHA224,
        ],
        ciphers=[
            SymmetricKeyAlgorithm.AES256,
            SymmetricKeyAlgorithm.AES192,
            SymmetricKeyAlgorithm.AES128,
        ],
        compression=[
            CompressionAlgorithm.ZLIB,
            CompressionAlgorithm.BZ2,
            CompressionAlgorithm.ZIP,
            CompressionAlgorithm.Uncompressed,
        ],
    )
    return key


def encrypt_pgp_message(public_key: str, message: str) -> str:
    import pgpy

    pgp_key, _ = pgpy.PGPKey.from_blob(public_key)
    plain_message = pgpy.PGPMessage.new(message)
    pgp_message = pgp_key.encrypt(plain_message)

    return str(pgp_message)


def decrypt_pgp_message(private_key: str, encrypted_message: str) -> str:
    import pgpy

    pgp_private_key, _ = pgpy.PGPKey.from_blob(private_key)
    pgp_message = pgpy.PGPMessage.from_blob(encrypted_message)
    plain_message = pgp_private_key.decrypt(pgp_message)

    return str(plain_message.message)


def assert_pgp_email(
    email_str: str,
    email: str,
    name: str,
    subject: str,
    message: str,
    sender_email: str,
    to_email: str,
    to_name: str,
    private_key: pgpy.PGPKey,
    sender_public_key: Optional[pgpy.PGPKey],
) -> Optional[str]:
    p = parser.Parser()
    mail = p.parsestr(email_str)

    mail_headers = {k: v for k, v in mail.items()}
    assert (
        'multipart/encrypted; protocol="application/pgp-encrypted"; charset="UTF-8";'
        in mail_headers["Content-Type"]
    )
    assert mail_headers["MIME-Version"] == "1.0"
    assert mail_headers["Date"]
    assert name in mail_headers["From"]
    assert sender_email in mail_headers["From"]
    assert to_email in mail_headers["To"]
    assert to_name in mail_headers["To"]
    assert name in mail_headers["Reply-To"]
    assert email in mail_headers["Reply-To"]
    assert mail_headers["Subject"]

    pgp_mime = cast(Any, mail.get_payload(0))
    pgp_mime_headers = {k: v for k, v in pgp_mime._headers}
    assert pgp_mime_headers["Content-Type"] == "application/pgp-encrypted"
    assert pgp_mime_headers["Content-Description"] == "PGP/MIME version identification"
    assert pgp_mime._payload == "Version: 1\n"

    pgp_enc_body = cast(Any, mail.get_payload(1))
    pgp_enc_body_headers = {k: v for k, v in pgp_enc_body._headers}
    assert (
        pgp_enc_body_headers["Content-Type"]
        == 'application/octet-stream; name="encrypted.asc"'
    )
    assert pgp_enc_body_headers["Content-Description"] == "OpenPGP encrypted message"
    assert (
        pgp_enc_body_headers["Content-Disposition"]
        == 'inline; filename="encrypted.asc"'
    )
    assert "-----BEGIN PGP MESSAGE-----" in pgp_enc_body._payload
    assert "-----END PGP MESSAGE-----" in pgp_enc_body._payload

    dec_message_str = decrypt_pgp_message(str(private_key), pgp_enc_body._payload)

    dec_email = p.parsestr(dec_message_str)
    dec_email_headers = {k: v for k, v in dec_email.items()}
    assert "multipart/mixed" in dec_email_headers["Content-Type"]

    dec_email_body = cast(Any, dec_email.get_payload(0))
    dec_email_body_headers = {k: v for k, v in dec_email_body._headers}
    assert dec_email_body_headers["Content-Type"] == 'text/plain; charset="utf-8"'
    assert dec_email_body_headers["MIME-Version"] == "1.0"
    assert dec_email_body_headers["Content-Transfer-Encoding"] == "base64"

    dec_email_body_payload = b64decode(dec_email_body._payload).decode("utf-8")
    assert dec_email_body_payload == message

    pub_key = None
    if dec_email.is_multipart() and sender_public_key:
        dec_email_attach = cast(Any, dec_email.get_payload(1))
        dec_email_attach_headers = {k: v for k, v in dec_email_attach._headers}
        assert (
            dec_email_attach_headers["Content-Type"]
            == 'application/pgp-keys; name="publickey.asc"'
        )
        assert (
            dec_email_attach_headers["Content-Disposition"]
            == 'attachment; filename="publickey.asc"'
        )
        assert dec_email_attach_headers["Content-Transfer-Encoding"] == "base64"

        pub_key = b64decode(dec_email_attach._payload).decode("utf-8")
        assert pub_key == str(sender_public_key)

    return pub_key


def assert_plain_email(
    email_str: str,
    email: str,
    name: str,
    subject: str,
    message: str,
    sender_email: str,
    to_email: str,
    to_name: str,
) -> None:
    p = parser.Parser()
    mail = p.parsestr(email_str)

    mail_headers = {k: v for k, v in mail.items()}
    assert "multipart/mixed" in mail_headers["Content-Type"]
    assert mail_headers["MIME-Version"] == "1.0"
    assert mail_headers["Date"]
    assert name in mail_headers["From"]
    assert sender_email in mail_headers["From"]
    assert to_email in mail_headers["To"]
    assert to_name in mail_headers["To"]
    assert name in mail_headers["Reply-To"]
    assert email in mail_headers["Reply-To"]
    assert mail_headers["Subject"]
    assert mail.preamble == "This is a multi-part message in MIME format.\n"

    body = cast(Any, mail.get_payload(0))
    body_headers = {k: v for k, v in body._headers}
    assert body_headers["Content-Type"] == 'text/plain; charset="utf-8"'
    assert body_headers["MIME-Version"] == "1.0"
    assert body_headers["Content-Transfer-Encoding"] == "base64"

    body_payload = b64decode(body._payload).decode("utf-8")
    assert body_payload == message
