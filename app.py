from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from app.resources.mysql.query import *
from app.resources.instance.query import Instance
from app import app, api
from app.common.auth import Login, Logout
from app.resources.kubernetes.kubernetes import Kubernetes
from app.resources.kubernetes.Upload import Upload

api.add_resource(Mysql, '/mysql')
api.add_resource(Instance, '/instance')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Kubernetes, '/k8s')
api.add_resource(Upload, '/upload')

if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
    # app.run(host='0.0.0.0')
