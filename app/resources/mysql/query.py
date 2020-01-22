import mysql.connector
from config import APP_ENV, configs
from flask_login import login_required, current_user
from app.common.auth import query_user, query_ldap_user
from DBUtils.PooledDB import PooledDB
from flask_restful import Resource, reqparse
from app.common.abort import generate_response
from app.models.db import database_info, record_sql
import json
from app import db


class Mysql(Resource):
    decorators = [login_required]
    __pool = None

    def __init__(self):
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('sql', type=str, required=True)
        self.parser.add_argument('database', type=str)
        self.parser.add_argument('sqls', type=str, required=True)
        self.parser.add_argument('instance', type=str, required=True)
        self.args = self.parser.parse_args()
        # 判断用户是否有数据库权限
        if (current_user.type == 'account'):
            self.execute_instances = query_user(current_user.id).execute_instances
            self.read_instances = query_user(current_user.id).read_instances
        if (current_user.type == 'ldap'):
            self.execute_instances = query_ldap_user(current_user.id).execute_instances
            self.read_instances = query_ldap_user(current_user.id).read_instances
        # 判断用户数据库（读/写）权限
        self.instance = None
        if self.read_instances:
            if self.args['instance'] in self.read_instances.split(','):
                self.instance = database_info.query.filter(database_info.instance == self.args['instance']).first()
                self.db_host = self.instance.ip
                self.db_user = self.instance.read_user
                self.db_pass = self.instance.read_password
        if self.execute_instances:
            if self.args['instance'] in self.execute_instances.split(','):
                self.instance = database_info.query.filter(database_info.instance == self.args['instance']).first()
                self.db_host = self.instance.ip
                self.db_user = self.instance.execute_user
                self.db_pass = self.instance.execute_password
        self.base = self.args['database']

    def __getConn(self):
        if Mysql.__pool is None:
            __pool = PooledDB(creator=mysql.connector, mincached=1, maxcached=20,
                              host=self.db_host, port=self.instance.port, user=self.db_user,
                              passwd=self.db_pass,
                              db=self.base, charset=configs[APP_ENV].charset)
        return __pool.connection()

    def post(self):
        # 没有实例权限直接返回错误
        if self.instance is None or self.instance == '':
            return generate_response(status=400, data='实例不存在或用户权限不足')
        # 获取数据库连接
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()
        result = []
        k = 0
        # sql = self.args['sql']
        sqls = self.args['sqls']
        # SQL语句格式检查
        try:
            sql_json = json.loads(sqls)
        except Exception as err:
            return generate_response(status=400, data='数据格式不正确')
        else:
            for sql in sql_json['sqls']:
                if sql is None or sql == '':
                    return generate_response(status=400, data='请输入语句')
                type = sql.split()[0].lower()
                type2 = sql.split()[1].lower()
                # print(sql)
                # 开始执行SQL语句
                try:
                    self._cursor.execute(sql)
                    # 判断是否需要commit操作
                    if type == 'insert' or type == 'delete':
                        self._conn.commit()
                except Exception as err:
                    return generate_response(data=str(err), status=400)
                else:
                    record = record_sql(user=current_user.id, sql=sql)
                    db.session.add(record)
                    db.session.commit()
                    index = self._cursor.description
                    if type == 'show' or type == 'select':
                        data = self._cursor.fetchall()
                    else:
                        data = self._cursor.fetchone()
        finally:
            # 关闭数据库连接
            self._cursor.close()
            self._conn.close()
        # print(index)
        # print(data)
        # 数据格式化处理
        if type == 'show' and type2 == 'create':
            # print(index)
            i = 0
            for j in str(data[0]).split('\\n'):
                row = {}
                row['Create Table'] = j
                row['key'] = i
                i = i + 1
                result.append(row)
            return generate_response(result)
        if type == 'show' and type2 != 'create':
            if data is not None:
                i = 0
                for j in data:
                    row = {}
                    for res in index:
                        row[res[0]] = j[0]
                        row['key'] = i
                    result.append(row)
                    i = i + 1
                return generate_response(result)
        if type == 'select':
            if data is not None:
                for j in data:
                    i = 0
                    row = {}
                    for res in index:
                        row[res[0]] = j[i]
                        i += 1
                    row['key'] = k
                    k = k + 1
                    result.append(row)
                return generate_response(result)
        else:
            if data is None:
                return generate_response(data='执行成功', status=201)
