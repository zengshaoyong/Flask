from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from app.common.abort import generate_response
from app import limiter
from app.common.auth import query_user, query_ldap_user
from app import db
from app.models.db import redis_info


class Manager_mysql(Resource):
    decorators = [limiter.limit(limit_value="2 per second", key_func=lambda: current_user.id,
                                error_message=generate_response(data='访问太频繁', status='429')), login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, required=True)
        self.parser.add_argument('ip', type=str)
        self.parser.add_argument('port', type=str)
        self.parser.add_argument('name', type=str, required=True)
        self.parser.add_argument('password', type=str)
        self.args = self.parser.parse_args()
        # 判断用户是否有redis权限
        self.auth = 0
        if current_user.type == 'ldap':
            self.auth = query_ldap_user(current_user.id).currentAuthority
        if current_user.type == 'account':
            self.auth = query_user(current_user.id).currentAuthority

    def get(self):
        if int(self.auth) < 10:
            return generate_response(status=400, data='用户权限不足')
