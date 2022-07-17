from datetime import datetime
from uuid import uuid4

from flask_login import UserMixin
from blog_on_flask import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


def uuid4_string(func):
    def wrapper(*args, **kwargs):
        uuid4_to_string = str(func(*args, **kwargs))
        return uuid4_to_string

    return wrapper


uuid4 = uuid4_string(uuid4)


@login_manager.user_loader
def load_user(user_uid):
    return User.query.get(user_uid)


class User(db.Model, UserMixin):
    uid = db.Column(db.String(36), primary_key=True, default=uuid4)
    username = db.Column(db.String(24), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(64), nullable=True, default='default.png')
    password = db.Column(db.String(64), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_id(self):
        try:
            return self.uid
        except AttributeError:
            raise NotImplementedError("No `uid` attribute - override `get_id`") from None

    def __repr__(self):
        return f'Пользователь с логином: {self.username} | email: {self.email}'

    def get_reset_token(self, expires_sec=3600):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_uid': self.uid}).decode(encoding='utf-8')

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_uid = serializer.loads(token)['user_uid']
        except Exception:
            return None
        return User.query.get(user_uid)


class Post(db.Model):
    uid = db.Column(db.String(36), primary_key=True, default=uuid4)
    title = db.Column(db.String(128), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(256), nullable=True)
    user_uid = db.Column(db.String(36), db.ForeignKey('user.uid'), nullable=False)
    comments = db.relationship('Comment', backref='title', lazy='dynamic')

    def __repr__(self):
        return f'Пост: {self.title} | {self.date_posted}'


class Comment(db.Model):
    uid = db.Column(db.String(36), primary_key=True, default=uuid4)
    content = db.Column(db.String(512))
    post_uid = db.Column(db.String(36), db.ForeignKey('post.uid'), nullable=False)
    user_uid = db.Column(db.String(36), db.ForeignKey('user.uid'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Like(db.Model):
    __table_args__ = (db.PrimaryKeyConstraint('user_uid', 'post_uid', name='CompositePkForLike'),)

    user_uid = db.Column(db.String(36), db.ForeignKey('user.uid'), nullable=False)
    post_uid = db.Column(db.String(36), db.ForeignKey('post.uid'), nullable=False)
