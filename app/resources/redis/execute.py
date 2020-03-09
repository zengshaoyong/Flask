from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from app.common.abort import generate_response
from app import limiter
from app.common.auth import query_user, query_ldap_user
from app.models.db import redis_info
import redis
from redis import ConnectionPool


class Redis(Resource):
    decorators = [limiter.limit(limit_value="10 per second", key_func=lambda: current_user.id,
                                error_message=generate_response(data='访问太频繁', status='429')), login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('key', type=str, required=True)
        self.parser.add_argument('type', type=str, required=True)
        self.parser.add_argument('redis', type=str, required=True)
        self.args = self.parser.parse_args()
        # 判断用户是否有redis权限
        self.redis = None
        if current_user.type == 'ldap':
            self.redis = query_ldap_user(current_user.id).redis
            # print(self.redis)

    def get(self):
        if self.redis == '' or self.redis is None:
            return generate_response(status=400, data='用户权限不足')
        if self.args['type'] == 'get_instance':
            return generate_response(data=self.redis.split(','))
        if self.args['redis'] in self.redis.split(','):
            instance = redis_info.query.filter(redis_info.name == self.args['redis']).first()
            redis_host = instance.ip
            redis_port = instance.port
            password = instance.password
        else:
            return generate_response(status=400, data='用户权限不足')
        Pool = ConnectionPool(host=redis_host, port=redis_port, password=password, max_connections=100)
        conn = redis.Redis(connection_pool=Pool)
        results = []
        if self.args['type'] == 'scan':
            result = conn.scan_iter(match=self.args['key'], count=None)
            for i in result:
                results.append(i.decode())
            return generate_response(results)
        if self.args['type'] == 'get':
            value = conn.get(self.args['key'])
            ttl = conn.ttl(self.args['key'])
            # result = conn.get(self.args['key'])
            if value is not None:
                results.append({'value': value.decode()})
                results.append({'expire': ttl})
            return generate_response(results)
