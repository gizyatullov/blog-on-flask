from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required

from blog_on_flask import db
from blog_on_flask.models import Post, Comment, Like
from .forms import PostForm, CommentForm, LikeForm
from .utils import save_photo_post

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
        if form.photo.data:
            post.photo = save_photo_post(form.photo.data)
        db.session.add(post)
        db.session.commit()
        flash(message='Ваш пост создан!', category='success')
        return redirect(url_for('posts.all_post'))
    context = {
        'page_title': 'Создать новый пост',
        'form': form,
    }
    return render_template('create-post.html', **context)


@posts.route('/post/<string:post_uid>', methods=('GET', 'POST',))
@login_required
def post(post_uid):
    post = Post.query.get_or_404(post_uid)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(content=comment_form.content.data, post_uid=post_uid, user_uid=current_user.uid)
        db.session.add(comment)
        db.session.commit()
        flash('Ваш комментарий добавлен!', 'success')
        return redirect(url_for('posts.post', post_uid=post_uid))

    context = {
        'page_title': f'Подробно про пост: {post.title}',
        'post': post,
        'comment_form': comment_form,
        'like_form': LikeForm(),
        'like_count': Like.query.filter_by(post_uid=post_uid).count()
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


@posts.route('/post/comment-del/<string:comment_uid>', methods=('POST',))
@login_required
def del_comment(comment_uid):
    comment = Comment.query.get_or_404(comment_uid)
    if comment.user_uid == current_user.uid:
        post_uid = comment.post_uid
        db.session.delete(comment)
        db.session.commit()
        flash('Ваш комментарий был удален!', 'success')
        return redirect(url_for('posts.post', post_uid=post_uid))
    return redirect(url_for('errors.error_403'))


@posts.route('/post/<string:post_uid>/like', methods=('POST',))
@login_required
def like_post(post_uid):
    post = Post.query.get_or_404(post_uid)

    if post.author == current_user:
        flash('Вы не можете поставить лайк т.к. пост создали Вы сами', 'warning')
    elif Like.query.filter_by(user_uid=current_user.uid, post_uid=post_uid).count():
        Like.query.filter_by(user_uid=current_user.uid, post_uid=post_uid).delete()
        db.session.commit()
        flash('Вам больше не нравится этот пост.', 'success')
    else:
        like = Like(user_uid=current_user.uid, post_uid=post_uid)
        db.session.add(like)
        db.session.commit()
        flash('Вам нравится этот пост.', 'success')

    return redirect(url_for('posts.post', post_uid=post_uid))
