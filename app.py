from app.resources.datasearch.query import *
from app import app, api
from gevent import monkey
from gevent.pywsgi import WSGIServer
from app.common.auth import Login, Logout
from app.resources.deploy.manger import Manage
from app.resources.deploy.deployips import Deployips
from app.resources.deploy.uploads import Upload

monkey.patch_all()

server = WSGIServer(('0.0.0.0', 5000), app)

api.add_resource(Mysql, '/mysql')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Manage, '/manage')
api.add_resource(Deployips, '/deployips')
api.add_resource(Upload, '/upload')

if __name__ == '__main__':
    server.serve_forever()
