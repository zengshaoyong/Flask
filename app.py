from gevent import monkey

monkey.patch_all()

from app.resources.datasearch.query import *
from app import app, api
from gevent.pywsgi import WSGIServer
from app.common.auth import Login, Logout
from app.resources.kubernetes.kubernetes import Kubernetes
from app.resources.kubernetes.Upload import Upload

server = WSGIServer(('0.0.0.0', 5000), app)
server.start()

api.add_resource(Mysql, '/mysql')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Kubernetes, '/k8s')
api.add_resource(Upload, '/upload')

if __name__ == '__main__':
    server.serve_forever()
    # app.run(host='0.0.0.0')
