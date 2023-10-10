from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_session import Session
from flask_socketio import SocketIO
from .auth import auth
from .models import UserModel
from .config import Config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config.from_object(Config)
    socketio = SocketIO(app, cors_allowed_origins="*", port=8000)
    Session(app)
    bootstrap = Bootstrap(app)
    login_manager.init_app(app)
    app.register_blueprint(auth)
    return socketio, app