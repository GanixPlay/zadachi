from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = IntegerField('Id руководителя')
    job = StringField('Описание работы')
    work_size = IntegerField('Объём работы в часах')
    categories = IntegerField('Cat')
    collaborators = StringField('Участники')
    end_date = DateTimeField('Дата завершения')
    is_finished = BooleanField('Работа завершена?')
    submit = SubmitField('Добавить')
