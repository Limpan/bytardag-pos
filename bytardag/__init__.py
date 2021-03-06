import logging

from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


__version__ = "0.1.0"

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Logga in för att visa denna sida."
moment = Moment()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    sentry_sdk.init(
        dsn=app.config["SENTRY_DSN"],
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    from bytardag.filters import Filters

    filters = Filters()
    filters.init_app(app)

    from bytardag.main import bp as main_bp

    app.register_blueprint(main_bp)

    from bytardag.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from bytardag.user import bp as user_bp

    app.register_blueprint(user_bp, url_prefix="/user")

    if not app.debug and not app.testing:
        # Log to STDOUT
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(logging.INFO)

    app.logger.info("Bytardag POS startup.")

    return app


from bytardag import models  # noqa: E402, F401, I100, I202
