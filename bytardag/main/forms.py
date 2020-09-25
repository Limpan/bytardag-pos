from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired

from bytardag import db
from bytardag.models import Seller


class RegisterForm(FlaskForm):
    seller = StringField("Sälj-ID", validators=[DataRequired()])
    amount = IntegerField("Pris", validators=[DataRequired()])
    submit = SubmitField("Spara")

    def validate_seller(self, field):
        sid = db.session.query(Seller).filter_by(seller_id=field.data).first()
        if not sid:
            raise ValidationError("Ogiltigt sälj-ID.")


class VerifyForm(FlaskForm):
    missing = SubmitField("Kvittorad saknas!")
    submit = SubmitField("Verifiera")
