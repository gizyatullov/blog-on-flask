from flask import render_template, Blueprint, redirect, url_for, flash

from .forms import WriteMeForm
from .utils import send_me_message

contacts = Blueprint('contacts', __name__)


@contacts.route('/contacts', methods=['GET', 'POST'])
def index():
    form = WriteMeForm()

    if form.validate_on_submit():
        try:
            send_me_message(form)
        except Exception:
            flash('При отправке Вашего сообщения возникла непредвиденная ошибка, попробуйте позже!', 'error')
        else:
            flash('Ваше сообщение успешно отправлено!', 'success')
        return redirect(url_for('contacts.index'))

    context = {
        'page_title': 'контакты',
        'form': form,
    }
    return render_template('contact.html', **context)
