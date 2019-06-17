from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from app.common.format import Format
import os

ALLOWED_EXTENSIONS = set(['war', 'jar'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class Upload(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('file', type=FileStorage, location='files', required=True, help='请选择文件')

    def post(self):
        args = self.parser.parse_args()
        file = args['file']
        if file and allowed_file(file.filename):
            # print(file.filename)
            file.save(os.path.join('D:/uploads', file.filename))
            return Format('上传成功')
        return Format('请选择正确的文件')
