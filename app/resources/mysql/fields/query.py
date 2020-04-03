import mysql.connector
from config import APP_ENV, configs
from flask_login import login_required, current_user
from app.common.auth import query_user, query_ldap_user
from DBUtils.PooledDB import PooledDB
from flask_restful import Resource, reqparse
from app.common.abort import generate_response
from app.models.db import database_info


class Field(Resource):
    decorators = [login_required]

    __pool = None

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('database', type=str, required=True)
        self.parser.add_argument('table', type=str, required=True)
        self.parser.add_argument('instance', type=str, required=True)
        self.args = self.parser.parse_args()
        # 判断用户是否有数据库权限
        databases = []
        database = database_info.query.all()
        for i in database:
            databases.append(i.instance)
        if current_user.type == 'account':
            self.execute_instances = query_user(current_user.id).execute_instances
            self.read_instances = query_user(current_user.id).read_instances
        if current_user.type == 'ldap':
            self.execute_instances = query_ldap_user(current_user.id).execute_instances
            self.read_instances = query_ldap_user(current_user.id).read_instances
        # 判断用户数据库（读/写）权限
        self.instance = None
        if self.read_instances:
            if self.args['instance'] in [val for val in databases if val in self.read_instances.split(',')]:
                self.instance = database_info.query.filter(database_info.instance == self.args['instance']).first()
                self.db_host = self.instance.ip
                self.db_user = self.instance.read_user
                self.db_pass = self.instance.read_password
        if self.execute_instances:
            if self.args['instance'] in [val for val in databases if val in self.execute_instances.split(',')]:
                self.instance = database_info.query.filter(database_info.instance == self.args['instance']).first()
                self.db_host = self.instance.ip
                self.db_user = self.instance.execute_user
                self.db_pass = self.instance.execute_password
        self.base = self.args['database']

    def __getConn(self):
        if Field.__pool is None:
            __pool = PooledDB(creator=mysql.connector, mincached=1, maxcached=20,
                              host=self.db_host, port=self.instance.port, user=self.db_user,
                              passwd=self.db_pass,
                              db=self.base, charset=configs[APP_ENV].charset)
        return __pool.connection()

    def get(self):
        # 没有实例权限直接返回错误
        if self.instance is None or self.instance == '':
            return generate_response(status=400, data='实例不存在或用户权限不足')
        # 获取数据库连接
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()
        sql = 'SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = "%s" AND TABLE_NAME = "%s"' % (
            self.args['database'], self.args['table'])
        # print(sql)
        self._cursor.execute(sql)
        data = self._cursor.fetchall()
        k = 0
        result = []
        for i in data:
            row = {'key': k, 'field': i[0]}
            result.append(row)
            k = k + 1
        return generate_response(result)
