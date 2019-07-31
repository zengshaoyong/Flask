from flask_restful import Resource, reqparse
from app.resources.deploy.manger import query_app
from shutil import copyfile
from config import configs, APP_ENV
from app.common.format import Success, Failed

warsrc = configs[APP_ENV].warsrc
wardst = configs[APP_ENV].wardst
jarsrc = configs[APP_ENV].jarsrc
jardst = configs[APP_ENV].jardst


# 把应用包从上传文件夹拷贝到发布文件夹中
class Cpfile(Resource):
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
            dst = wardst
            re = '.war'
        if section == 'jar':
            src = jarsrc
            dst = jardst
            re = '.jar'
        app = app.split(',')
        # print(app)
        for i in app:
            if query_app(i.replace(re, '')):
                copyfile(src + i, dst + i)
        return Success('')
