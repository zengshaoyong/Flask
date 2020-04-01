from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from app.common.abort import generate_response
from app import limiter
from app.common.auth import query_user, query_ldap_user
from app import db
from app.models.db import LdapUser


class Manager_user(Resource):
    decorators = [limiter.limit(limit_value="2 per second", key_func=lambda: current_user.id,
                                error_message=generate_response(data='访问太频繁', status='429')), login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, required=True)
        self.parser.add_argument('username', type=str, required=True)
        self.parser.add_argument('authority', type=str, required=True)
        self.parser.add_argument('namespace', type=str, required=True)
        self.parser.add_argument('group', type=str, required=True)
        self.parser.add_argument('execute_instances', type=str, required=True)
        self.parser.add_argument('read_instances', type=str, required=True)
        self.parser.add_argument('redis', type=str, required=True)
        self.args = self.parser.parse_args()
        # 判断用户是否有权限
        self.auth = 0
        if current_user.type == 'ldap':
            self.auth = query_ldap_user(current_user.id).currentAuthority
        if current_user.type == 'account':
            self.auth = query_user(current_user.id).currentAuthority

    def get(self):
        if int(self.auth) < 100:
            return generate_response(status=400, data='用户权限不足')
        if self.args['type'] == 'query':
            results = []
            result = LdapUser.query.all()
            for i in result:
                row = {'key': str(i.id), 'username': str(i.username), 'authority': str(i.currentAuthority),
                       'namespace': str(i.namespace), 'group': str(i.group),
                       'execute_instances': str(i.execute_instances), 'read_instances': str(i.read_instances),
                       'redis': str(i.redis)}
                results.append(row)
            return generate_response(results)
        if self.args['type'] == 'del':
            user = LdapUser.query.filter(LdapUser.username == self.args['username']).first()
            db.session.delete(user)
            db.session.commit()
            return generate_response(status=201)
        if self.args['type'] == 'modify':
            user = LdapUser.query.filter(LdapUser.username == self.args['username']).first()
            user.currentAuthority = self.args['authority']
            user.namespace = self.args['namespace']
            user.group = self.args['group']
            user.execute_instances = self.args['execute_instances']
            user.read_instances = self.args['read_instances']
            user.redis = self.args['redis']
            db.session.commit()
            return generate_response(status=201)
