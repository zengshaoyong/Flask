from flask_restful import Resource, reqparse
from app.resources.deploy.manger import query_app
from shutil import copyfile
from app.common.format import Success, Failed


class Cpfile(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('app', type=str, required=True)

    def get(self):
        args = self.parser.parse_args()
        app = args['app']
        src = 'D:/uploads/'
        dst = 'D:/wars/'
        app = app.split(',')
        # print(app)
        for i in app:
            if query_app(i.replace('.war', '')):
                copyfile(src + i, dst + i)
        return Success('')
