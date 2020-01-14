from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from app.common.abort import generate_response
from werkzeug.utils import secure_filename
from flask_login import login_required
import os

ALLOWED_EXTENSIONS = set(['yaml'])
basedir = os.getcwd()
file_dir = os.path.join(basedir, 'upload')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class Upload(Resource):
    decorators = [login_required]

    def post(self):
        # print(file_dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()
        file = args['file']
        if file.filename == '':
            return generate_response('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # print(filename)
            upload_path = os.path.join(file_dir, filename)
            # print(upload_path)
            file.save(upload_path)
            return generate_response(filename)
