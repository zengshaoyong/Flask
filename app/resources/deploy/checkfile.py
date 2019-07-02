from flask_restful import Resource
from app.common.format import Success
import os


class Checkfile(Resource):

    def get(self):
        path = 'D:/uploads'
        dirs = os.listdir(path)
        result = {}
        results = []
        for file in dirs:
            # print(file)
            # print(os.path.getctime(path + '/' + file))
            # print(os.path.getsize(path + '/' + file))
            createtime = os.path.getctime(path + '/' + file)
            size = os.path.getsize(path + '/' + file)
            result['filename'] = file
            result['createtime'] = createtime
            result['size'] = size
            results.append(result)
        return Success(results)
