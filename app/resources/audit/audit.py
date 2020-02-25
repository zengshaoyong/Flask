import time

from flask_login import login_required
from flask_restful import Resource, reqparse

from app.common.abort import generate_response
from app.models.db import record_sql


def record(username, st_time, end_time):
    # result = record_sql.query.filter(record_sql.user == username, record_sql.time >= '2020-02-24 10:05:50',
    #                                  record_sql.time <= '2020-02-24 11:09:44').all()
    if username is not None:
        result = record_sql.query.filter(record_sql.user == username, record_sql.time >= local_time(st_time),
                                         record_sql.time <= local_time(end_time)).all()
    if username is None:
        result = record_sql.query.filter(record_sql.time >= local_time(st_time),
                                         record_sql.time <= local_time(end_time)).all()
    return result


def local_time(timestamp):
    # 转换成时间数组
    time_array = time.localtime(int(timestamp))
    # 转换成时间
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return localtime


class Audit(Resource):
    decorators = [login_required]

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
                   'sql': str(i.sql)}
            results.append(row)
        return generate_response(results)
