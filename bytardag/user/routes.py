from flask import current_app, flash, redirect, render_template, url_for

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
        user = User(
            username=form.username.data,
            name=form.name.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        current_app.logger.info("Created user {}.".format(user.username))
        flash("Skapade användare {}".format(user.username))
        return redirect(url_for("user.list"))
    return render_template("user/create.html", form=form)
