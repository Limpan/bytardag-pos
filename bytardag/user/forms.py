from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    username = StringField("Användarnamn", validators=[DataRequired()])
    password = StringField("Lösenord", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Skapa")
