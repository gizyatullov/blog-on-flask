from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from blog_on_flask import db, bcrypt
from blog_on_flask.models import User, Post
from blog_on_flask.users.forms import (RegistrationForm, LoginForm,
                                       UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from .utils import save_picture, send_reset_email

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
        return redirect(url_for('posts.all_post'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('posts.all_post'))
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


@users.route('/user/<string:username>', methods=['GET'])
@login_required
def user_posts(username: str):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    context = {
        'page_title': f'Посты пользователя: {user.username}',
        'posts': posts,
        'user': user,
    }
    return render_template('user-posts.html', **context)


@users.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_post'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'На почту {user.email} отправлено письмо с инструкциями по сбросу пароля.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',
                           page_title='сброс пароля',
                           form=form)


@users.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_post'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Это недействительный или просроченный токен.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был обновлен! Теперь Вы можете авторизоваться.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',
                           page_title='Сброс пароля',
                           form=form)
