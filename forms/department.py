from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, Email

class DepartmentForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    chief = IntegerField('ID начальника', validators=[Optional()])
    members = StringField('Члены (ids через запятую)', validators=[Optional()])
    email = StringField('E-mail', validators=[Optional(), Email()])
    submit = SubmitField('Создать отдел')
