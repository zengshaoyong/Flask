from flask_restful import Resource, reqparse
from app.common.format import Success
from config import configs, APP_ENV
import os
import time

upload_war = configs[APP_ENV].warsrc
upload_jar = configs[APP_ENV].jarsrc


def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)

# 查询已上传应用的信息
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
        results = []
        for file in dirs:
            # print(file)
            result = {}
            # print(os.path.getctime(path + '/' + file))
            # print(os.path.getsize(path + '/' + file))
            createtime = os.path.getctime(path + file)
            size = os.path.getsize(path + file)
            result['filename'] = file
            result['createtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(createtime))
            result['size'] = formatSize(size)
            results.append(result)
            # print(results)
        return Success(results)
