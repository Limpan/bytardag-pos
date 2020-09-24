from flask import url_for
from flask_login import current_user
import pytest

from bytardag import __version__
from bytardag.models import User


def login(client, username, password):
    return client.post(
        url_for("auth.login"),
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def logout(client):
    return client.get(url_for("auth.logout"), follow_redirects=True)


def test_version():
    assert __version__ == "0.1.0"


def test_app_exists(app):
    assert app is not None


def test_app_is_testing(app):
    assert app.config["TESTING"]


def test_index_page(client):
    assert 200 < client.get(url_for("main.index")).status_code < 400


def test_redirect_to_login(client):
    rv = client.get(url_for("main.index"))
    assert rv.status_code == 302


@pytest.mark.skip
def test_logged_in(client, db):
    user = User(username="test", password="qwerty")
    db.session.add(user)
    db.session.commit()

    rv = login(client, "test", "qwerty")
    assert current_user.id == user.id
    assert "Du har loggats in.".encode() in rv.data
