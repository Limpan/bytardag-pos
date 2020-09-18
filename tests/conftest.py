import pytest

from bytardag import create_app


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        yield app
