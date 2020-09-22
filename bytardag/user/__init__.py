from flask import Blueprint

bp = Blueprint("user", __name__)

from bytardag.user import routes  # noqa: E402, F401, I100, I202
