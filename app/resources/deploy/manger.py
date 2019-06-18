from flask_restful import Resource, reqparse
from app.common.format import Success, Failed
from app.models.db import Ipaddrs


def query_app(name):
    app = Ipaddrs.query.filter(Ipaddrs.name == name).first()
    # print(app)
    return app


def query_all():
    app = Ipaddrs.query.all()
    # print(app[0].name, app[0].ips)
    return app


class Manage(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('action', type=str, required=True)
        self.parser.add_argument('app', type=str)
        self.parser.add_argument('ips', type=str)

    def get(self):
        args = self.parser.parse_args()
        action = args['action']
        app = args['app']
        ips = args['ips']
        results = {}
        if action == 'query_all':
            result = query_all()
            for i in result:
                results[i.name] = i.ips.split(',')
            return Success(results)
        result = query_app(app)
        if result is not None:
            if action == 'query':
                results[result.name] = result.ips.split(',')
                return Success(results)
            if action == 'delete':
                result.delete_app(result)
                return Success('delete successfully')
            if action == 'add' and ips is not None:
                Ipaddrs.add_app(app, ips)
                return Success('add successfully')
            if action == 'update' and ips is not None:
                result.update_app(ips)
                return Success('update successfully')
        return Failed('please input correct app name')
