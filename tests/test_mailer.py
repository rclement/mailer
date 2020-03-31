import pytest

from mailer import mailer


def test_send_pgp_message_encryption_failed(faker):
    from . import utils

    pgp_key = utils.generate_pgp_key_pair(faker.name(), faker.email())

    m = mailer.Mailer(
        faker.email(),
        faker.email(),
        faker.name(),
        faker.hostname(),
        faker.port_number(),
        False,
        False,
        faker.user_name(),
        faker.password(),
        pgp_key,
    )

    with pytest.raises(RuntimeError):
        m.send_email(faker.email(), faker.name(), faker.text(), faker.text(), None)
