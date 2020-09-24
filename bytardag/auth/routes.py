from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from bytardag import db
from bytardag.auth import bp
from bytardag.auth.forms import LoginForm
from bytardag.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            current_app.logger.info(
                "Failed login attempt {}.".format(form.username.data)
            )
            flash("Ogiltigt användarnamn eller lösenord.")
            return redirect(url_for("auth.login"))
        current_app.logger.info("Logging in user {}.".format(user.username))
        login_user(user)
        flash("Du har loggats in.")
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    current_app.logger.info("Logging out user {}.".format(current_user.username))
    logout_user()
    return redirect(url_for("main.index"))
