from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from app.common.abort import generate_response
from app import limiter
from app.common.auth import query_user, query_ldap_user
from app import db
from app.models.db import redis_info


class Manager_redis(Resource):
    decorators = [limiter.limit(limit_value="2 per second", key_func=lambda: current_user.id,
                                error_message=generate_response(data='访问太频繁', status='429')), login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, required=True)
        self.parser.add_argument('ip', type=str, required=True)
        self.parser.add_argument('port', type=str, required=True)
        self.parser.add_argument('name', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)
        self.args = self.parser.parse_args()
        # 判断用户是否有权限
        self.auth = 0
        if current_user.type == 'ldap':
            self.auth = query_ldap_user(current_user.id).currentAuthority
        if current_user.type == 'account':
            self.auth = query_user(current_user.id).currentAuthority

    def get(self):
        if int(self.auth) < 10:
            return generate_response(status=400, data='用户权限不足')
        if self.args['type'] == 'query':
            results = []
            result = redis_info.query.all()
            for i in result:
                row = {'key': str(i.id), 'name': str(i.name), 'ip': str(i.ip), 'port': str(i.port),
                       'password': str(i.password)}
                results.append(row)
            return generate_response(results)
        if self.args['type'] == 'add':
            redis = redis_info(ip=self.args['ip'], port=self.args['port'],
                               name=self.args['name'],
                               password=self.args['password'])
            db.session.add(redis)
            db.session.commit()
        if self.args['type'] == 'del':
            redis = redis_info.query.filter(redis_info.instance == self.args['name']).first()
            db.session.delete(redis)
            db.session.commit()
        if self.args['type'] == 'modify':
            redis = redis_info.query.filter(redis_info.instance == self.args['name']).first()
            redis.ip = self.args['ip']
            redis.port = self.args['port']
            redis.name = self.args['name']
            redis.password = self.args['password']
            db.session.commit()