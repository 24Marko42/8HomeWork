from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    surname = StringField('Фамилия')
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired(), NumberRange(min=0, max=120)])
    position = StringField('Должность')
    speciality = StringField('Профессия')
    address = StringField('Адрес')
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), EqualTo('password_again', message='Пароли не совпадают')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    about = TextAreaField('О себе')
    submit = SubmitField('Зарегистрироваться')
