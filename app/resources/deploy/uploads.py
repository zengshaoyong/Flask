from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from app.common.format import Success, Failed
from app.resources.deploy.manger import query_app
import os

ALLOWED_EXTENSIONS = set(['war', 'jar'])

warsrc = 'D:/autotest/upload_war/'
jarsrc = 'D:/autotest/upload_jar/'


# 检查应用名字是否正确
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 检查数据库是否存在此应用的信息
def check(filename):
    return query_app(filename.rsplit('.', 1)[0])


class Upload(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('file', type=FileStorage, location='files', required=True, help='请选择文件')

    def post(self):
        args = self.parser.parse_args()
        file = args['file']
        if check(file.filename) and allowed_file(file.filename):
            # print(file.filename)
            tmp = file.filename.rsplit('.', 1)[1]
            if tmp == 'war':
                path = warsrc
            if tmp == 'jar':
                path = jarsrc
            file.save(os.path.join(path, file.filename))
            return Success('上传成功')
        return Failed('请选择正确的文件')
