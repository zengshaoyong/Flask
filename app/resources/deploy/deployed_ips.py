from flask_restful import Resource, reqparse
from app.resources.deploy.manger import query_app, query_all
from app.common.format import Success, Failed


class Deployed_ips(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('app', type=str, required=True)

    def get(self):
        args = self.parser.parse_args()
        app = args['app']
        ips = []
        result = query_app(app)
        if result:
            filename = 'D:\%s' % app
            with open(filename) as file:
                for line in file:
                    line = line.split(' ')
                    if (line.__len__() == 3):
                        ips.append(line[0])
                return Success(ips)
        else:
            return Failed('请输入正确的应用名')
