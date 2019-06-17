from app.models.user import User
from app import login_manager
from flask_login import login_user, logout_user
from flask_restful import Resource, reqparse
from flask_login import login_required
from flask import session, flash
from app.common.format import Format
from app.models.db import Userinfo


def query_user(username):
    user = Userinfo.query.filter(Userinfo.username == username).first()
    print(user)
    return user


@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username
        return curr_user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return Format('请登陆')


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)

    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        print(username)
        user = query_user(username)
        # 验证表单中提交的用户名和密码
        if user is not None:
            if user.check_password(args['password']):
                curr_user = User()
                curr_user.id = username
                login_user(curr_user)
                session.permanent = True
                return Format('login successfully')
                flash('login successfully')
            return Format('Wrong password')
            flash('Wrong password')
        return Format('Wrong username')
        flash('Wrong username')


class Logout(Resource):
    decorators = [login_required]

    def get(self):
        logout_user()
        return Format('logout successfully')
