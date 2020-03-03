from flask import Flask
import flask_restful
from flask_login import LoginManager, current_user
# from flask_cache import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
from app.common.errors import errors
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from config import configs, APP_ENV
from flask_cors import CORS
from app.common.abort import my_abort

login_manager = LoginManager()

app = Flask(__name__)
api = Api(app, errors=errors)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = configs[APP_ENV].SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=30)
login_manager.init_app(app)
login_manager.session_protection = 'strong'
# cache.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = configs[APP_ENV].SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SQLALCHEMY_COMMIT_TEARDOWN = True
db = SQLAlchemy(app)
flask_restful.abort = my_abort

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["600 per minute", "10 per second"],
)
