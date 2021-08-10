import pytest

from base64 import urlsafe_b64encode
from faker import Faker
from pydantic import ValidationError

from mailer import settings


def test_pgp_public_key_valid(monkeypatch: pytest.MonkeyPatch, faker: Faker) -> None:
    from . import utils

    pgp_key = utils.generate_pgp_key_pair(faker.name(), faker.email())
    pub_key = urlsafe_b64encode(str(pgp_key.pubkey).encode("utf-8")).decode("utf-8")
    monkeypatch.setenv("PGP_PUBLIC_KEY", pub_key)

    s = settings.Settings()
    assert str(s.pgp_public_key) == str(pgp_key.pubkey)


def test_pgp_public_key_private(monkeypatch: pytest.MonkeyPatch, faker: Faker) -> None:
    from . import utils

    pgp_key = utils.generate_pgp_key_pair(faker.name(), faker.email())
    prv_key = urlsafe_b64encode(str(pgp_key).encode("utf-8")).decode("utf-8")
    monkeypatch.setenv("PGP_PUBLIC_KEY", prv_key)

    with pytest.raises(ValidationError):
        settings.Settings()


def test_pgp_public_key_invalid(monkeypatch: pytest.MonkeyPatch, faker: Faker) -> None:
    from base64 import urlsafe_b64encode

    pgp_key = urlsafe_b64encode(faker.binary()).decode("utf-8")
    pub_key = urlsafe_b64encode(pgp_key.encode("utf-8")).decode("utf-8")
    monkeypatch.setenv("PGP_PUBLIC_KEY", pub_key)

    with pytest.raises(ValidationError):
        settings.Settings()
