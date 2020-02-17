from app.models.user import User
from app import login_manager
from ldap3 import Server, Connection, ALL
from flask_login import login_user, logout_user, current_user, login_required
from flask_restful import Resource, reqparse
from flask import session
from app.common.abort import generate_response, login_response
from app.models.db import Userinfo, LdapUser, db


def query_user(username):
    user = Userinfo.query.filter(Userinfo.username == username).first()
    return user


def query_ldap_user(username):
    user = LdapUser.query.filter(LdapUser.username == username).first()
    return user


def query_ldap(username, password):
    server = Server('ldap01.thinkinpower.net', use_ssl=True, get_info=ALL)
    username = "uid=%s,ou=People,dc=rfchina,dc=com" % (username)
    try:
        Connection(server, username, password, auto_bind=True)
        res = 'success'
    except Exception as err:
        res = str(err)
    finally:
        return res


@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username
        curr_user.type = 'account'
        return curr_user
    if query_ldap_user(username) is not None:
        curr_user = User()
        curr_user.id = username
        curr_user.type = 'ldap'
        return curr_user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return login_response(status='401', message='请登陆')


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
            res = query_ldap(username, password)
            if res == 'success':
                user = query_ldap_user(username)
                if user is None:
                    new_user = LdapUser(username=username, currentAuthority='0', namespace='default', group='test',
                                        execute_instances='', read_instances='')
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
