from flask import url_for

from bytardag import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_app_exists(client):
    assert 200 < client.get(url_for("main.index")).status_code < 400
