from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

__version__ = "0.1.0"

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Logga in för att visa denna sida."
moment = Moment()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    from bytardag.main import blueprint as main_blueprint

    app.register_blueprint(main_blueprint)

    from bytardag.auth import blueprint as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app


from bytardag import models  # noqa: E402, F401, I100
