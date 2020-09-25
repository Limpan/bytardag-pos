from flask import (
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    render_template_string,
    request,
    url_for,
)
from flask_login import current_user, login_required
import pendulum
from sqlalchemy import and_, func
from werkzeug.datastructures import MultiDict

from bytardag import db
from bytardag.decorators import admin_required
from bytardag.main import bp
from bytardag.main.forms import RegisterForm, VerifyForm
from bytardag.models import Row, Sheet


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = pendulum.now()
        db.session.commit()


@bp.route("/")
@login_required
def index():
    num_sheets = db.session.query(Sheet).count()
    #    num_open_sheets = db.session.query(Sheet).filter_by(closed=None).count()
    num_unsigned_sheets = (
        db.session.query(Sheet)
        .filter(Sheet.closed is not None, Sheet.signed_by is None)
        .count()
    )

    num_owned_sheets = current_user.sheets.count()
    num_unsigned_owned_sheets = (
        db.session.query(Sheet)
        .filter(Sheet.owner == current_user, Sheet.signed_by.is_(None))
        .count()
    )
    open_sheet = (
        db.session.query(Sheet)
        .filter(Sheet.owner == current_user, Sheet.closed.is_(None))
        .first()
    )

    return render_template(
        "main/index.html",
        sheets=current_user.sheets,
        open_sheet=open_sheet,
        num_owned_sheets=num_owned_sheets,
        num_unsigned_owned_sheets=num_unsigned_owned_sheets,
        num_sheets=num_sheets,
        #                           num_open_sheets=num_open_sheets,
        num_unsigned_sheets=num_unsigned_sheets,
    )


@bp.route("/entry/<int:id>", methods=["GET", "POST"])
@login_required
def entry(id):
    if request.is_json:
        form = RegisterForm(MultiDict(request.get_json()))
        if form.validate():
            current_app.logger.debug("Successfully validated.")
            sheet = Sheet.query.filter_by(id=id).first()
            row = Row(seller=form.seller.data.upper(), amount=form.amount.data)
            sheet.rows.append(row)
            db.session.add(row)
            db.session.commit()
            current_app.logger.info(
                "Added row #{} for sheet #{}".format(row.id, sheet.id)
            )
            num_rows = (
                db.session.query(Row)
                .join(Sheet.rows)
                .filter(Sheet.id == sheet.id)
                .count()
            )
            data = {
                "status": "ok",
                "added_value": {"seller": row.seller, "amount": row.amount},
                "rendered_string": render_template_string(
                    '{% from "macros.html" import render_row %}{{ render_row(seller, amount)|safe }}',  # noqa: B950
                    seller=row.seller,
                    amount=row.amount,
                ),
                "num_rows": num_rows,
            }
            return jsonify(data)
        current_app.logger.debug("Failed validation. Payload %s" % request.get_json())
        messages = [
            {"field": field.id, "errors": field.errors}
            for field in [form.seller, form.amount]
            if field.errors
        ]
        return jsonify({"status": "error", "messages": messages}), 400

    form = RegisterForm()

    sheet = db.session.query(Sheet).filter_by(id=id).one()

    if not sheet:
        abort(404)

    if sheet.closed:
        flash("Arket är stängt.")
        return redirect(url_for("main.index"))

    num_rows = (
        db.session.query(Row).join(Sheet.rows).filter(Sheet.id == sheet.id).count()
    )

    return render_template("main/entry.html", form=form, sheet=sheet, num_rows=num_rows)


@bp.route("/verify")
@login_required
def verify():
    sheets = (
        db.session.query(Sheet)
        .filter(
            and_(
                Sheet.owner != current_user,
                Sheet.closed.isnot(None),
                Sheet.signed_by.is_(None),
                Sheet.missing_value.isnot(True),
            )
        )
        .all()
    )

    return render_template("main/verify.html", sheets=sheets)


@bp.route("/entry/<int:id>/verify", methods=["GET", "POST"])
@login_required
def verify_entry(id):
    sheet = db.session.query(Sheet).get_or_404(id)

    if sheet.owner.id == current_user.id:
        flash("Du kan inte kontrollera ditt eget ark.")
        return redirect(url_for("main.verify"))

    if not sheet.closed:
        flash("Arket är inte stängt ännu.")
        return redirect(url_for("main.verify"))

    if sheet.signee:
        flash("Arket är redan kontrollerat.")
        return redirect(url_for("main.verify"))

    form = VerifyForm()

    if form.validate_on_submit():
        if form.missing.data:
            sheet.missing_value = True
            db.session.commit()
            current_app.logger.warning("Ark #{} saknar kvittorader.".format(id))
            flash("Ark #{} har markerats för kontroll.".format(id))
            return redirect(url_for("main.verify"))
        else:
            sheet.signee = current_user
            sheet.signed_at = pendulum.now()
            db.session.commit()
            current_app.logger.info("Verifierar ark #{}.".format(id))
            flash("Ark #{} har verifierats.".format(id))
            return redirect(url_for("main.verify"))

    return render_template("main/verify_sheet.html", form=form, sheet=sheet)


@bp.route("/entry/<int:id>/close")
@login_required
def close_sheet(id):
    sheet = db.session.query(Sheet).filter_by(id=id).first()

    if sheet.rows.count() == 0:
        flash("Arket har inga rader.")
        return redirect(url_for("main.entry", id=id))

    if sheet:
        sheet.closed = pendulum.now()
        db.session.commit()
        current_app.logger.info(f"Closing sheet #{sheet.id}.")
        flash(f"Ark {id} har stängts.")

    return redirect(url_for("main.index"))


@bp.route("/start_sheet")
@login_required
def start_sheet():
    # Check for open sheet for user.
    sheet = Sheet(owner=current_user)
    db.session.add(sheet)
    db.session.commit()
    current_app.logger.info(f"Creating sheet #{sheet.id}.")
    return redirect(url_for("main.entry", id=sheet.id))


@bp.route("/sheet/<int:id>")
@login_required
def sheet(id):
    sheet = db.session.query(Sheet).filter_by(id=id).first_or_404()
    return render_template("main/sheet.html", sheet=sheet)


@bp.route("/sheet")
@login_required
def sheets():
    sheets = db.session.query(Sheet).all()
    return render_template("main/sheets.html", sheets=sheets)


@bp.route("/seller")
@login_required
def list_sellers():
    sellers = db.session.query(Row.seller).distinct().order_by(Row.seller.asc()).all()

    return render_template("main/list_sellers.html", sellers=sellers)


@bp.route("/seller/<id>")
@login_required
def seller(id):
    rows = db.session.query(Row).filter_by(seller=id.upper()).all()
    stats = db.session.query(func.sum(Row.amount)).filter_by(seller=id.upper()).one()

    return render_template(
        "main/seller.html", seller_id=id.upper(), rows=rows, stats=stats
    )


@bp.route("/missing_value")
@admin_required
def missing_value():
    sheets = db.session.query(Sheet).filter(Sheet.missing_value.is_(True)).all()
    return render_template("main/missing_value.html", sheets=sheets)


@bp.route("/status")
def status():
    if request.is_json:
        num_sheets = db.session.query(Sheet).filter(Sheet.signed_by.is_(None)).count()
        num_verified_sheets = (
            db.session.query(Sheet).filter(Sheet.signed_at.isnot(None)).count()
        )
        num_error_sheets = (
            db.session.query(Sheet).filter(Sheet.missing_value.is_(True)).count()
        )

        data = {
            "status": "ok",
            "values": [num_sheets, num_verified_sheets, num_error_sheets],
        }
        return jsonify(data)

    return render_template("main/status.html")
