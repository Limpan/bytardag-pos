import tempfile

import pytest

from bytardag import cli
from bytardag.models import Seller, User


@pytest.fixture
def runner(app):
    """Fixture for command-line interface."""
    cli.register(app)

    return app.test_cli_runner()


def test_cli_succeeds(runner):
    """It exits with a status code of zero."""
    result = runner.invoke()
    assert result.exit_code == 0


def test_user_add(runner, db):
    """Test that `flask user add` works."""
    result = runner.invoke(args=["user", "add", "test", "qwerty"])
    user = db.session.query(User).filter_by(username="test").first()
    assert "Created user" in result.output
    assert user.verify_password("qwerty") is True


@pytest.mark.skip
def test_sid_init(runner, db):
    """Import SIDs from text file."""
    with tempfile.TemporaryFile(mode="w") as fp:
        fp.write("A-01\nA-03\nB-03\nC-01\n")
        fp.seek(0)

        result = runner.invoke(args=["sid", "init"], file=fp)

    assert "Added 4 seller IDs to database." in result.output

    assert db.session.query(Seller.id).count() == 4

    assert db.session.query(Seller).filter_by(seller_id="A-01").one()
    assert db.session.query(Seller).filter_by(seller_id="A-03").one()
    assert db.session.query(Seller).filter_by(seller_id="B-03").one()
    assert db.session.query(Seller).filter_by(seller_id="C-01").one()
