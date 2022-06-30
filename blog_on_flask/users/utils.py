import os
from pathlib import Path

from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from blog_on_flask import Conf, mail


def save_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f'{random_hex}{f_ext}'
    picture_path = os.path.join(current_app.root_path, str(Path('static', 'profile_pics')), picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()

    message_body = f"""
    Чтобы сбросить пароль, перейдите по ссылке: {url_for('users.reset_token', token=token, _external=True)}.
    Если Вы не делали этот запрос тогда просто проигнорируйте это письмо и никаких изменений не будет.
    """

    message = Message('Запрос на сброс пароля.',
                      sender=Conf.SENDER,
                      recipients=[user.email])
    message.body = message_body
    mail.send(message)
