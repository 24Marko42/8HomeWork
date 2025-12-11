from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class DepartmentForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    chief = IntegerField('ID начальника', validators=[DataRequired()])
    members = StringField('Члены (через запятую)')
    email = StringField('Email')
    submit = SubmitField('Добавить')