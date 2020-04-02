from app.models.db import database_info
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_login import login_required, current_user
from app.common.auth import query_user, query_ldap_user
from app.common.abort import generate_response


class Instance(Resource):
    decorators = [login_required]

    def __init__(self):
        if current_user.type == 'account':
            self.execute_instances = query_user(current_user.id).execute_instances
            self.read_instances = query_user(current_user.id).read_instances
        if current_user.type == 'ldap':
            self.execute_instances = query_ldap_user(current_user.id).execute_instances
            self.read_instances = query_ldap_user(current_user.id).read_instances

    def get(self):
        execute_instances = []
        read_instances = []
        databases = []
        result = database_info.query.all()
        for i in result:
            databases.append(i.instance)
        # print(databases)
        if self.execute_instances:
            execute_instances = self.execute_instances.split(',')
        if self.read_instances:
            read_instances = self.read_instances.split(',')
        instances = list(set(execute_instances).union(set(read_instances)))
        final = [val for val in databases if val in instances]
        return generate_response(final)
