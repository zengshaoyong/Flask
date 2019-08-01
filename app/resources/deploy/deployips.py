from flask_restful import Resource, reqparse
from app.resources.deploy.manger import query_app, query_all
from app.common.format import Success, Failed
from config import configs, APP_ENV
from flask import flash

war = configs[APP_ENV].ip_war
jar = configs[APP_ENV].ip_jar


# 写入IP地址到 ansible
class Deployips(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('action', type=str, required=True)
        self.parser.add_argument('section', type=str, required=True)
        self.parser.add_argument('app', type=str)
        # 单独部署某些IP时用
        self.parser.add_argument('ips', type=str)

    def get(self):
        args = self.parser.parse_args()
        action = args['action']
        section = args['section']
        app = args['app']
        ips = args['ips']
        if section == 'war':
            path = war
            type = 'war'
        if section == 'jar':
            path = jar
            type = 'jar'
        # results = query_all()
        if action == 'all':
            result = query_all()
            for i in result:
                # print(i.type)
                if i.type == type:
                    filename = path + '%s' % i.name
                    with open(filename, 'w') as f:
                        f.write('[%s]\n' % i.name)
                        results = i.ips.split(',')
                        for j in results:
                            f.write(j + ' ' + 'ansible_ssh_user=cssuser ansible_ssh_pass=Wandaph@9000' + '\n')
                            flash('初始化应用：%s成功' % i.name)
            return Success('初始化所有应用成功')

        result = query_app(app)
        if action == 'one' and result is not None:
            if ips:
                ips = ips.split(',')
                filename = path + '%s' % result.name
                with open(filename, 'w') as f:
                    f.write('[%s]\n' % result.name)
                    results = result.ips.split(',')
                    for i in ips:
                        # print(i)
                        if i in results:
                            f.write(i + ' ' + 'ansible_ssh_user=cssuser ansible_ssh_pass=Wandaph@9000' + '\n')
                return Success('初始化应用：%s 成功' % result.name)
            else:
                filename = path + '%s' % result.name
                with open(filename, 'w') as f:
                    f.write('[%s]\n' % result.name)
                    results = result.ips.split(',')
                    for i in results:
                        f.write(i + ' ' + 'ansible_ssh_user=cssuser ansible_ssh_pass=Wandaph@9000' + '\n')
                return Success('初始化应用：%s 成功' % result.name)
