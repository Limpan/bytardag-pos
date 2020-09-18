from flask import Blueprint

blueprint = Blueprint("auth", __name__)

from bytardag.auth import routes  # noqa: E402, F401
