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
        if (current_user.type == 'account'):
            self.group = query_user(current_user.id).group
        if (current_user.type == 'ldap'):
            self.group = query_ldap_user(current_user.id).group
        self.database = database_info.query.filter(database_info.group == self.group).first()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query', type=str)
        self.parser.add_argument('database', type=str)
        self.args = self.parser.parse_args()
        self.base = self.args['database']

        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()

    def __getConn(self):
        if Mysql.__pool is None:
            __pool = PooledDB(creator=mysql.connector, mincached=1, maxcached=20,
                              host=self.database.ip, port=self.database.port, user=self.database.user,
                              passwd=self.database.password,
                              db=self.base, charset=configs[APP_ENV].charset)
        return __pool.connection()

    # @marshal_with(resource_fields, envelope='data')
    def post(self):
        result = []
        sql = self.args['query']
        try:
            self._cursor.execute(sql)
        except Exception as err:
            return generate_response(str(err))
            # print(str(err))
        else:
            index = self._cursor.description
            data = self._cursor.fetchall()
        finally:
            self._cursor.close()
            self._conn.close()
        if sql == 'show databases' or sql == 'show tables':
            for res in data:
                result.append(res[0])
            return generate_response(result)
        else:
            for j in data:
                i = 0
                row = {}
                for res in index:
                    row[res[0]] = j[i]
                    i += 1
                result.append(row)
            return generate_response(result)
