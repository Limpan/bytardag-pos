from flask import render_template

from . import bp
from .forms import UserForm
from .. import db
from ..decorators import admin_required
from ..models import User


@bp.route("/list")
@admin_required
def list():
    users = db.session.query(User).all()
    return render_template("user/list.html", users=users)


@bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():
    form = UserForm()
    if form.validate_on_submit():
        pass
    return render_template("user/create.html", form=form)
