from flask import Flask
from flask_login import LoginManager
from flask_cache import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
from app.common.errors import errors
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from config import configs, APP_ENV

login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
api = Api(app, errors=errors)
app.config['SECRET_KEY'] = configs[APP_ENV].SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=10)
login_manager.init_app(app)
login_manager.session_protection = 'strong'
cache.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = configs[APP_ENV].SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True
db = SQLAlchemy(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute", "2 per second"],
)
