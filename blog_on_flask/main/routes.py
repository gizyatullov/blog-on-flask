from flask import render_template, Blueprint

from blog_on_flask.models import User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    context = {
        'page_title': 'главная',
    }
    return render_template('index.html', **context)


@main.route('/examples')
def examples():
    context = {
        'page_title': 'примеры',
    }
    return render_template('examples.html', context=context)


@main.route('/page')
def page():
    context = {
        'page_title': 'страница',
    }
    return render_template('page.html', context=context)


@main.route('/another-page')
def another_page():
    context = {
        'page_title': 'еще одна страница',
    }
    return render_template('register.html', context=context)


@main.route('/contact')
def contact():
    context = {
        'page_title': 'контакты',
    }
    return render_template('contact.html', context=context)
