from flask_restful import Resource, reqparse
from app.common.format import Success, Failed
from app.models.db import Ipaddrs

def query_app(name):
    app = Ipaddrs.query.filter(Ipaddrs.name == name).first()
    # print(app)
    return app

class App_ips(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('app', type=str, required=True)

    def get(self):
        args = self.parser.parse_args()
        app = args['app']
        result = query_app(app)
        result = result.ips.split(',')
        # print(result)
        return Success(result)


