from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CategoryForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired()])
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')