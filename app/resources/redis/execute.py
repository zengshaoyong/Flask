from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from app.common.abort import generate_response
from app import limiter
from app.common.auth import query_user, query_ldap_user
import redis
from redis import ConnectionPool


class Redis(Resource):
    decorators = [limiter.limit(limit_value="10 per second", key_func=lambda: current_user.id,
                                error_message=generate_response(data='访问太频繁', status='429')), login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('key', type=str, required=True)
        self.parser.add_argument('type', type=str, required=True)
        self.args = self.parser.parse_args()
        # 判断用户是否有redis权限
        self.redis = None
        if current_user.type == 'ldap':
            self.redis = query_ldap_user(current_user.id).redis

    def get(self):
        if self.redis == '' or self.redis is None:
            return generate_response(status=400, data='用户权限不足')
        redis_host = self.redis.split(':')[0]
        redis_port = self.redis.split(':')[1]
        Pool = ConnectionPool(host=redis_host, port=redis_port, max_connections=100)
        conn = redis.Redis(connection_pool=Pool)
        results = []
        if self.args['type'] == 'scan':
            result = conn.scan_iter(match=self.args['key'], count=None)
            for i in result:
                results.append(i.decode())
            return generate_response(results)
        if self.args['type'] == 'get':
            result = conn.get(self.args['key'])
            if result is not None:
                results.append(result.decode())
            return generate_response(results)
