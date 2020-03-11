import time

from flask_login import login_required, current_user
from flask_restful import Resource, reqparse
from app import limiter

from app.common.abort import generate_response
from app.models.db import record_redis


def record(username, st_time, end_time):
    # result = record_sql.query.filter(record_sql.user == username, record_sql.time >= '2020-02-24 10:05:50',
    #                                  record_sql.time <= '2020-02-24 11:09:44').all()
    if username != '':
        result = record_redis.query.filter(record_redis.user == username, record_redis.time >= local_time(st_time),
                                           record_redis.time <= local_time(end_time)).all()
    if username == '':
        result = record_redis.query.filter(record_redis.time >= local_time(st_time),
                                           record_redis.time <= local_time(end_time)).all()
    return result


def local_time(timestamp):
    # 转换成时间数组
    time_array = time.localtime(int(timestamp))
    # 转换成时间
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return localtime


class Audit_redis(Resource):
    decorators = [limiter.limit(limit_value="3 per second", key_func=lambda: current_user.id,
                                error_message=generate_response(data='访问太频繁', status='429')), login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('st_time', type=str, required=True)
        self.parser.add_argument('end_time', type=str, required=True)
        self.args = self.parser.parse_args()

    def get(self):
        result = record(self.args['username'], self.args['st_time'], self.args['end_time'])
        results = []
        for i in result:
            row = {'key': str(i.id), 'username': str(i.user), 'time': str(i.time), 'instance': str(i.instance),
                   'action': str(i.action), 'keys': str(i.key)}
            results.append(row)
        return generate_response(results)