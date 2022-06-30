from flask_mail import Message

from blog_on_flask import Conf, mail


def send_me_message(form):
    message_body = f"""
    Вам написали сообщение (обратную связь) с блога на flask!\n
        Имя: {form.your_name.data}\n
        Email: {form.your_email.data}\n
        Сообщение: {form.message.data}\n
    """
    message = Message('Message with blog-on-flask',
                      sender=Conf.SENDER,
                      recipients=[Conf.MY_EMAIL])
    message.body = message_body
    mail.send(message)
