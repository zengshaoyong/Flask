from flask_login import login_required, current_user
from app.common.auth import query_user, query_ldap_user
from flask_restful import Resource, reqparse
from app.common.abort import generate_response


class Current_user(Resource):
    decorators = [login_required]

    def __init__(self):
        if (current_user.type == 'account'):
            self.userid = query_user(current_user.id).id
            self.username = query_user(current_user.id).username
        if (current_user.type == 'ldap'):
            self.userid = query_ldap_user(current_user.id).id
            self.username = query_ldap_user(current_user.id).username

    def get(self):
        return generate_response({'name': self.username, 'userid': self.userid})
