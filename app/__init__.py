from flask import Flask
from flask_bootstrap import Bootstrap
from .auth import auth
from app.config import Config
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)
    login_manager.init_app(app)
    app.register_blueprint(auth)
    return app

