from flask_restful import Resource, reqparse
import os
from config import configs, APP_ENV
from app.common.format import Success, Failed

warsrc = configs[APP_ENV].warsrc
jarsrc = configs[APP_ENV].jarsrc


# 删除发布文件夹下面的文件
class Rmfile(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('app', type=str, required=True)
        self.parser.add_argument('section', type=str, required=True)

    def get(self):
        args = self.parser.parse_args()
        app = args['app']
        section = args['section']
        if section == 'war':
            src = warsrc
        if section == 'jar':
            src = jarsrc
        os.remove(src + app)
        return Success('')
