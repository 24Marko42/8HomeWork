from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class JobForm(FlaskForm):
    team_leader = IntegerField('ID руководителя', validators=[DataRequired()])
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Объем работы (часы)', validators=[DataRequired()])
    collaborators = StringField('ID участников (через запятую)')
    is_finished = BooleanField('Завершена')
    categories = SelectMultipleField('Категории', coerce=int)
    submit = SubmitField('Сохранить')