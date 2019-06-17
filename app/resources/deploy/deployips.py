from flask_restful import Resource, reqparse
from app.resources.deploy.manger import query_app, query_all
from app.common.format import Format
from flask import flash


class Deployips(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('action', type=str, required=True)
        self.parser.add_argument('app', type=str)

    def get(self):
        args = self.parser.parse_args()
        action = args['action']
        app = args['app']
        result = query_app(app)
        # results = query_all()
        if action == 'one' and result is not None:
            filename = 'D:\%s' % result.name
            with open(filename, 'w') as f:
                f.write('[%s]\n' % result.name)
                results = result.ips.split(',')
                for i in results:
                    f.write(i + ' ' + 'ansible_ssh_user=cssuser ansible_ssh_pass=Wandaph@9000' + '\n')
            return Format('初始化应用：%s 成功' % result.name)
        if action == 'all':
            result = query_all()
            for i in result:
                filename = 'D:\%s' % i.name
                with open(filename, 'w') as f:
                    f.write('[%s]\n' % i.name)
                    results = i.ips.split(',')
                    for j in results:
                        f.write(j + ' ' + 'ansible_ssh_user=cssuser ansible_ssh_pass=Wandaph@9000' + '\n')
                        flash('初始化应用：%s成功' % i.name)
            return Format('初始化所有应用成功')
