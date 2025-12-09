from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional

class JobForm(FlaskForm):
    team_leader = IntegerField('ID тимлида', validators=[DataRequired()])
    job = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Объём (часы)', validators=[DataRequired()])
    collaborators = StringField('Коллабораторы (через запятую)', validators=[Optional()])
    is_finished = BooleanField('Завершена')
    submit = SubmitField('Добавить работу')
