from flask_restful import Resource, reqparse
from app.resources.deploy.manger import query_app
from shutil import copyfile
from app.common.format import Success, Failed

warsrc = 'D:/autotest/upload_war/'
wardst = 'D:/autotest/wars/'
war = '.war'
jarsrc = 'D:/autotest/upload_jar/'
jardst = 'D:/autotest/jars/'
jar = '.jar'


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
            re = war
        if section == 'jar':
            src = jarsrc
            dst = jardst
            re = jar
        app = app.split(',')
        # print(app)
        for i in app:
            if query_app(i.replace(re, '')):
                copyfile(src + i, dst + i)
        return Success('')
