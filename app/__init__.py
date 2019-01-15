'''
Boilerplate Python3 Flask SocketIO app

Janne Spijkervet, 2017
'''
from flask import Flask
from flask_socketio import SocketIO
from .info import Info
from .log import Log
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


__version__ = '1.0.0'

app_info = Info()
socketio = SocketIO()
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
log = Log(db)

def create_app(DB_PATH):
    from . import events

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + DB_PATH
    app.config['SECRET_KEY'] = 'Aqewur381!%*'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .views.index import index_bp
    from .views.login import login_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)

    socketio.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    return app
