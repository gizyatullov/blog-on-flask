from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class WriteMeForm(FlaskForm):
    your_name = StringField('Ваше имя', validators=(DataRequired(), Length(min=2, max=24),))
    your_email = EmailField('Ваш email', validators=(DataRequired(), Length(min=2, max=24), Email(),))
    message = TextAreaField('Сообщение', validators=(DataRequired(),))
    submit = SubmitField('Отправить')
