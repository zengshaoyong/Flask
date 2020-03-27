from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from app.common.abort import generate_response
from app import limiter
from app.common.auth import query_user, query_ldap_user
from app import db
from app.models.db import database_info


class Manager_mysql(Resource):
    decorators = [limiter.limit(limit_value="2 per second", key_func=lambda: current_user.id,
                                error_message=generate_response(data='访问太频繁', status='429')), login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, required=True)
        self.parser.add_argument('ip', type=str, required=True)
        self.parser.add_argument('port', type=str, required=True)
        self.parser.add_argument('read_user', type=str, required=True)
        self.parser.add_argument('read_password', type=str, required=True)
        self.parser.add_argument('execute_user', type=str, required=True)
        self.parser.add_argument('execute_password', type=str, required=True)
        self.parser.add_argument('instance', type=str, required=True)
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
            result = database_info.query.all()
            for i in result:
                row = {'key': str(i.id), 'instance': str(i.instance), 'ip': str(i.ip), 'port': str(i.port),
                       'read_user': str(i.read_user),
                       'read_password': str(i.read_password), 'execute_user': str(i.execute_user),
                       'execute_password': str(i.execute_password)}
                results.append(row)
            return generate_response(results)
        if self.args['type'] == 'add':
            database = database_info(instance=self.args['instance'], ip=self.args['ip'], port=self.args['port'],
                                     read_user=self.args['read_user'],
                                     read_password=self.args['read_password'],
                                     execute_user=self.args['execute_user'],
                                     execute_password=self.args['execute_password'])
            db.session.add(database)
            db.session.commit()
            return generate_response(status=201)
        if self.args['type'] == 'del':
            database = database_info.query.filter(database_info.instance == self.args['instance']).first()
            db.session.delete(database)
            db.session.commit()
            return generate_response(status=201)
        if self.args['type'] == 'modify':
            database = database_info.query.filter(database_info.instance == self.args['instance']).first()
            database.ip = self.args['ip']
            database.port = self.args['port']
            database.read_user = self.args['read_user']
            database.read_password = self.args['read_password']
            database.execute_user = self.args['execute_user']
            database.execute_password = self.args['execute_password']
            db.session.commit()
            return generate_response(status=201)
