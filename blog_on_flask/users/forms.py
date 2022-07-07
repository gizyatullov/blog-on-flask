from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from blog_on_flask.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=(DataRequired(), Length(min=2, max=21),))
    email = StringField('Email', validators=(DataRequired(), Email(),))
    password = PasswordField('Пароль', validators=(DataRequired(),))
    confirm_password = PasswordField('Подтвердите пароль', validators=(DataRequired(), EqualTo('password'),))
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'Логин «{username.data}» занят. Пожалуйста, выберите другой.xD')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'Этот email «{email.data}» занят. Пожалуйста, выберите другой.xD')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=(DataRequired(), Email(),))
    password = PasswordField('Пароль', validators=(DataRequired(),))
    remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Логин пользователя', validators=(DataRequired(), Length(min=2, max=21),))
    email = StringField('Email', validators=(DataRequired(), Email(),))
    picture = FileField('Обновить фото профиля', validators=(FileAllowed(('jpg', 'png',)),))
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if not username.data == current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f'Логин «{username.data}» занят. Пожалуйста, выберите другой.xD')

    def validate_email(self, email):
        if not email.data == current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'Этот email «{email.data}» занят. Пожалуйста, выберите другой.xD')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=(DataRequired(), Email(),))
    submit = SubmitField('Изменить пароль')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(f'Аккаунта с email «{email.data}» не существует.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=(DataRequired(),))
    confirm_password = PasswordField('Подтвердите пароль', validators=(DataRequired(), EqualTo('password'),))
    submit = SubmitField('Изменить пароль')
