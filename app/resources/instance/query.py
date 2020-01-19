from app.models.db import database_info
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_login import login_required, current_user
from app.common.auth import query_user, query_ldap_user
from app.common.abort import generate_response


class Instance(Resource):
    decorators = [login_required]

    def __init__(self):
        if (current_user.type == 'account'):
            self.instance = query_user(current_user.id).instances
        if (current_user.type == 'ldap'):
            self.instance = query_ldap_user(current_user.id).instances

    def get(self):
        instances = self.instance.split(',')
        return generate_response(instances)
