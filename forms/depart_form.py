from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class DepartForm(FlaskForm):
    title = StringField('Описание департамента')
    chief = IntegerField('Id капитана')
    members = StringField('Участники')
    email = StringField('Email')
    submit = SubmitField('Добавить')
