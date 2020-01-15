from app.models.user import User
from app import login_manager
from app import ldap_manager
from flask_login import login_user, logout_user
from flask_restful import Resource, reqparse
from flask_login import login_required
from flask import session
from app.common.abort import generate_response, login_response
from app.models.db import Userinfo, LdapUser
from app import db
from app.common.format import typeof
from app.common.menu import menu

def query_user(username):
    user = Userinfo.query.filter(Userinfo.username == username).first()
    # print(user)
    return user


def query_ldap_user(username):
    user = LdapUser.query.filter(LdapUser.username == username).first()
    return user


@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    user = User(dn, username, data)
    # users[dn] = user
    return user


@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username
        return curr_user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return generate_response('请登陆')


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('password')
        self.parser.add_argument('userName')
        self.parser.add_argument('type')
        self.args = self.parser.parse_args()

    def post(self):
        login_type = self.args['type']
        username = self.args['userName']
        password = self.args['password']
        if login_type == 'account':
            user = query_user(username)
            if user is not None:
                if user.check_password(password):
                    curr_user = User()
                    curr_user.id = username
                    login_user(curr_user)
                    session.permanent = True
                    return login_response(status='ok', currentAuthority=user.currentAuthority)
                    # return login_response(status='ok', menu=menu)
                return login_response(message='密码错误')
            return login_response(message='用户不存在')
        elif login_type == 'ldap':
            response = ldap_manager.authenticate(username, password)
            if typeof(response.user_id) == 'str':
                user = query_ldap_user(username)
                if user is None:
                    new_user = LdapUser(username=username, currentAuthority='guest', namespace='default')
                    db.session.add(new_user)
                    db.session.commit()
                    user = query_ldap_user(username)
                curr_user = User()
                curr_user.id = username
                login_user(curr_user)
                session.permanent = True
                return login_response(status='ok', currentAuthority=user.currentAuthority)
                # return login_response(status='ok', menu=menu)
            return login_response(message='用户名或密码错误')


class Logout(Resource):
    decorators = [login_required]

    def get(self):
        logout_user()
        return generate_response('logout successfully')
