import os

from config import Config
import pytest

from bytardag import create_app, db as _db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def db(app, request):
    """Session wide database connection."""
    _db.init_app(app)
    _db.create_all()
    _db.session.commit()
    # Add additional initialization code here...

    def teardown():
        _db.session.remove()
        _db.drop_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function", autouse=True)
def session(db, request):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
