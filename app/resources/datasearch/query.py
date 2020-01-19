import mysql.connector
from config import APP_ENV, configs
from flask_login import login_required, current_user
from DBUtils.PooledDB import PooledDB
from flask_restful import Resource, reqparse, fields, marshal_with
from app.common.abort import generate_response
from app.common.auth import query_user, query_ldap_user
from app.models.db import database_info

resource_fields = {
    'Id': fields.String,
    'User': fields.String,
    'Host': fields.String,
    'db': fields.String,
    'Command': fields.String,
    'Time': fields.String,
}


class Mysql(Resource):
    decorators = [login_required]
    __pool = None

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query', type=str, required=True)
        self.parser.add_argument('database', type=str)
        self.parser.add_argument('instance', type=str, required=True)
        self.args = self.parser.parse_args()
        self.instance = database_info.query.filter(database_info.instance == self.args['instance']).first()
        self.base = self.args['database']
        if self.instance is not None:
            self._conn = self.__getConn()
            self._cursor = self._conn.cursor()

    def __getConn(self):
        if Mysql.__pool is None:
            __pool = PooledDB(creator=mysql.connector, mincached=1, maxcached=20,
                              host=self.instance.ip, port=self.instance.port, user=self.instance.read_user,
                              passwd=self.instance.read_password,
                              db=self.base, charset=configs[APP_ENV].charset)
        return __pool.connection()

    # @marshal_with(resource_fields, envelope='data')
    def post(self):
        if self.instance is None or self.instance == '':
            return generate_response(status=400, data='请选择实例')
        result = []
        k = 0
        sql = self.args['query']
        if sql is None or sql == '':
            return generate_response(status=400, data='请输入语句')
        try:
            self._cursor.execute(sql)
        except Exception as err:
            return generate_response(data=str(err), status=400)
            # print(str(err))
        else:
            index = self._cursor.description
            data = self._cursor.fetchall()
        finally:
            self._cursor.close()
            self._conn.close()
        if sql == 'show databases' or sql == 'show tables':
            for j in data:
                row = {}
                for res in index:
                    row[res[0]] = j[0]
                result.append(row)
            return generate_response(result)
        else:
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
