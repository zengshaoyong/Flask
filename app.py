from gevent import monkey
from app.resources.datasearch.query import *
from app import app, api
from gevent.pywsgi import WSGIServer
from app.common.auth import Login, Logout
from app.resources.kubernetes.kubernetes import Kubernetes
from app.resources.kubernetes.Upload import Upload

# monkey.patch_all()

server = WSGIServer(('0.0.0.0', 5000), app)

api.add_resource(Mysql, '/mysql')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Kubernetes, '/k8s')
api.add_resource(Upload, '/upload')

if __name__ == '__main__':
    server.serve_forever()
