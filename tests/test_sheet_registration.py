from flask import url_for
import pytest

from bytardag.models import Sheet, User


def login(client, username, password):
    return client.post(
        url_for("auth.login"),
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def logout(client):
    return client.get(url_for("auth.logout"), follow_redirects=True)


@pytest.mark.skip
def test_create_sheet(client, db):
    user = User(username="test")
    user.password = "qwerty"
    db.session.add(user)
    db.session.commit()

    before = len(db.session.query(Sheet.id).all())

    login(client, "test", "qwerty")
    client.get(url_for("main.start_sheet"))

    after = len(db.session.query(Sheet.id).all())
    assert after - before == 1
