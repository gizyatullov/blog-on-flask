from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required

from blog_on_flask import db
from blog_on_flask.models import Post
from .forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/all-post', methods=('GET',))
@login_required
def all_post():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    context = {
        'page_title': 'все посты',
        'posts': posts,
    }
    return render_template('all-post.html', **context)


@posts.route('/post/new', methods=('GET', 'POST'))
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(message='Ваш пост создан!', category='success')
        return redirect(url_for('posts.all_post'))
    context = {
        'page_title': 'Создать новый пост',
        'form': form,
    }
    return render_template('create-post.html', **context)


@posts.route('/post/<string:post_uid>', methods=('GET',))
@login_required
def post(post_uid):
    post = Post.query.get_or_404(post_uid)
    context = {
        'page_title': f'Подробно про пост: {post.title}',
        'post': post,
    }
    return render_template('post.html', **context)


@posts.route('/post/<string:post_uid>/update', methods=('GET', 'POST'))
@login_required
def update_post(post_uid):
    post = Post.query.get_or_404(post_uid)
    if not post.author == current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Ваш пост обновлен!', 'success')
        return redirect(url_for('posts.post', post_uid=post.uid))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    context = {
        'page_title': f'Редактировать пост: {post.title}',
        'form': form,
    }
    return render_template('create-post.html', **context)


@posts.route('/post/<string:post_uid>/delete', methods=('POST',))
@login_required
def delete_post(post_uid):
    post = Post.query.get_or_404(post_uid)
    if not post.author == current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был удален!', 'success')
    return redirect(url_for('posts.all_post'))
