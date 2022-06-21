from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from blog_on_flask import db, bcrypt
from blog_on_flask.models import User, Post
from blog_on_flask.users.forms import (RegistrationForm, LoginForm,
                                       UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from .utils import save_picture

users = Blueprint('users', __name__)


@users.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваша учетная запись была создана!\nТеперь вы можете войти в систему.', 'success')
        return redirect(url_for('users.login'))

    context = {
        'page_title': 'регистрация',
        'form': form,
    }

    return render_template('register.html', **context)


@users.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('Войти не удалось. Пожалуйста, проверьте email и пароль', 'внимание')

    context = {
        'page_title': 'Войти',
        'form': form,
    }
    return render_template('login.html', **context)


@users.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')

    context = {
        'page_title': 'Аккаунт',
        'image_file': image_file,
        'form': form,
        'posts': posts,
        'user': user,
    }

    return render_template('account.html', **context)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
