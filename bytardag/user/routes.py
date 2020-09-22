from flask import render_template
from flask_login import login_required

from . import bp
from .forms import UserForm
from .. import db
from ..models import User


@bp.route("/list")
@login_required
def list():
    users = db.session.query(User).all()
    return render_template("user/list.html", users=users)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = UserForm()
    if form.validate_on_submit():
        pass
    return render_template("user/create.html", form=form)
