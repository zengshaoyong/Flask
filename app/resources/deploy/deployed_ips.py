from flask_restful import Resource, reqparse
from app.resources.deploy.manger import query_app
from app.common.format import Success, Failed
from config import configs, APP_ENV

war = configs[APP_ENV].ip_war
jar = configs[APP_ENV].ip_jar


# 检索已写入ansible的IP地址
class Deployed_ips(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('app', type=str, required=True)
        self.parser.add_argument('section', type=str, required=True)

    def get(self):
        args = self.parser.parse_args()
        app = args['app']
        section = args['section']
        ips = []
        if section == 'war':
            path = war
        if section == jar:
            path = jar
        result = query_app(app)
        if result:
            filename = '%s%s' % (path, app)
            with open(filename) as file:
                for line in file:
                    line = line.split(' ')
                    if (line.__len__() == 3):
                        ips.append(line[0])
                return Success(ips)
        else:
            return Failed('请输入正确的应用名')
