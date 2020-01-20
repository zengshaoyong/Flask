import mysql.connector
from config import APP_ENV, configs
from flask_login import login_required
from DBUtils.PooledDB import PooledDB
from flask_restful import Resource, reqparse
from app.common.abort import generate_response
from app.models.db import database_info
import json


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
        self.instance = database_info.query.filter(database_info.instance == self.args['instance']).first()
        self.base = self.args['database']
        # if self.instance is not None:
        #     self._conn = self.__getConn()
        #     self._cursor = self._conn.cursor()

    def __getConn(self):
        if Mysql.__pool is None:
            __pool = PooledDB(creator=mysql.connector, mincached=1, maxcached=20,
                              host=self.instance.ip, port=self.instance.port, user=self.instance.read_user,
                              passwd=self.instance.read_password,
                              db=self.base, charset=configs[APP_ENV].charset)
        return __pool.connection()

    def post(self):
        if self.instance is None or self.instance == '':
            return generate_response(status=400, data='请选择实例')
        result = []
        k = 0
        # sql = self.args['sql']
        sqls = self.args['sqls']
        # print(sqls)
        sql_json = json.loads(sqls)
        for sql in sql_json['sqls']:
            if self.instance is not None:
                self._conn = self.__getConn()
                self._cursor = self._conn.cursor()
            if sql is None or sql == '':
                return generate_response(status=400, data='请输入语句')
            type = sql.split()[0].lower()
            try:
                self._cursor.execute(sql)
                if type == 'insert' or type == 'delete':
                    self._conn.commit()
            except Exception as err:
                return generate_response(data=str(err), status=400)
            else:
                index = self._cursor.description
                if type == 'show' or type == 'select':
                    data = self._cursor.fetchall()
                else:
                    data = self._cursor.fetchone()
            finally:
                self._cursor.close()
                self._conn.close()
        if type == 'show':
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
