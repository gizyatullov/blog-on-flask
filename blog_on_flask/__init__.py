from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from .conf import Conf

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Conf)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .main.routes import main
    from .users.routes import users
    from .posts.routes import posts

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    return app
