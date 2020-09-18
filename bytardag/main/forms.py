from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    seller = StringField("Sälj-ID", validators=[DataRequired()])
    amount = IntegerField("Pris", validators=[DataRequired()])
    submit = SubmitField("Spara")


class VerifyForm(FlaskForm):
    missing = SubmitField("Kvittorad saknas!")
    submit = SubmitField("Verifiera")
