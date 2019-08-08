from flask_restful import Resource, reqparse
import os
from config import configs, APP_ENV
from app.common.format import Success, Failed

warsrc = configs[APP_ENV].wardst
jarsrc = configs[APP_ENV].jardst


# 在发布文件夹下创建空文件
class Touchfile(Resource):
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
        file = src + app + '.' + section
        if not os.path.exists(file):
            touch = open(file, 'w')
            touch.close()
            return Success('创建文件成功')
        return Success('文件已存在')
