from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField('Название', validators=(DataRequired(),))
    content = TextAreaField('Контент', validators=(DataRequired(),))
    photo = FileField('Фото', validators=(FileAllowed(('jpg', 'png',)),))
    submit = SubmitField('Создать')
