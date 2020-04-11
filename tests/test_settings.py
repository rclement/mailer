import pytest

from base64 import urlsafe_b64encode
from pydantic import ValidationError
from mailer import settings


def test_pgp_public_key_valid(faker):
    from . import utils

    pgp_key = utils.generate_pgp_key_pair(faker.name(), faker.email())
    pub_key = urlsafe_b64encode(str(pgp_key.pubkey).encode("utf-8")).decode("utf-8")
    values = {"pgp_public_key": pub_key}

    s = settings.Settings(**values)
    assert str(s.pgp_public_key) == str(pgp_key.pubkey)


def test_pgp_public_key_private(faker):
    from . import utils

    pgp_key = utils.generate_pgp_key_pair(faker.name(), faker.email())
    prv_key = urlsafe_b64encode(str(pgp_key).encode("utf-8")).decode("utf-8")
    values = {"pgp_public_key": prv_key}

    with pytest.raises(ValidationError):
        settings.Settings(**values)


def test_pgp_public_key_invalid(faker):
    from base64 import urlsafe_b64encode

    pgp_key = urlsafe_b64encode(faker.binary()).decode("utf-8")
    pub_key = urlsafe_b64encode(pgp_key.encode("utf-8")).decode("utf-8")
    values = {"pgp_public_key": pub_key}

    with pytest.raises(ValidationError):
        settings.Settings(**values)
