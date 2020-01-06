# __init__.py
from datetime import timedelta

from flask import Flask, Response
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    app.config['CORS_HEADERS'] = 'Content-Type, CookieX-Auth-Token, Origin, Accept, Authorization, access-control-allow-origin'
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        # do stuff
        return Response("Unauthorized", 302)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    CORS(app, resources=r'/*', allow_headers='Content-Type, Cookie, Set-Cookie, CookieX-Auth-Token, Origin, Accept, Authorization, access-control-allow-origin')

    return app