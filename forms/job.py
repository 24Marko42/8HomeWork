from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class JobForm(FlaskForm):
    team_leader = IntegerField('ID руководителя', validators=[DataRequired()])
    job = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Объем работы в часах', validators=[DataRequired()])
    collaborators = StringField('Участники (через запятую)')
    is_finished = BooleanField('Завершена')
    submit = SubmitField('Добавить')