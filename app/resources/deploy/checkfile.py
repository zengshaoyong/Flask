from flask_restful import Resource, reqparse
from app.common.format import Success
import os

upload_war = 'D:/autotest/upload_war/'
upload_jar = 'D:/autotest/upload_jar/'


class Checkfile(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('section', type=str, required=True)

    def get(self):
        args = self.parser.parse_args()
        section = args['section']
        if section == 'war':
            path = upload_war
        if section == 'jar':
            path = upload_jar
        dirs = os.listdir(path)
        result = {}
        results = []
        for file in dirs:
            # print(file)
            # print(os.path.getctime(path + '/' + file))
            # print(os.path.getsize(path + '/' + file))
            createtime = os.path.getctime(path + file)
            size = os.path.getsize(path + file)
            result['filename'] = file
            result['createtime'] = createtime
            result['size'] = size
            results.append(result)
        return Success(results)
