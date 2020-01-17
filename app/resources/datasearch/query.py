import mysql.connector
from config import APP_ENV, configs
from flask_login import login_required
from DBUtils.PooledDB import PooledDB
from flask_restful import Resource, reqparse, fields, marshal_with
from app.common.abort import generate_response

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
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query', type=str)

    def __getConn(self):
        if Mysql.__pool is None:
            __pool = PooledDB(creator=mysql.connector, mincached=1, maxcached=20,
                              host=configs[APP_ENV].host, port=configs[APP_ENV].port, user=configs[APP_ENV].user,
                              passwd=configs[APP_ENV].password,
                              db=configs[APP_ENV].database, charset=configs[APP_ENV].charset)
        return __pool.connection()

    # @marshal_with(resource_fields, envelope='data')
    def post(self):
        result = []
        row = {}
        i = 0
        args = self.parser.parse_args()
        sql = args['query']
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
        if sql == 'show databases':
            for res in data:
                result.append(res[0])
                i = i + 1
        if sql == 'show processlist':
            for res in index:
                row[res[0]] = data[0][i]
                i += 1
            result.append(row)
        else:
            for j in data:
                i = 0
                for res in index:
                    row[res[0]] = j[i]
                    i += 1
                result.append(row)
        return generate_response(result)


