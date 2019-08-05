from app.resources.datasearch.query import *
from app import app, api
from gevent import monkey
from gevent.pywsgi import WSGIServer
from app.common.auth import Login, Logout
from app.resources.deploy.manger import Manage
from app.resources.deploy.deployips import Deployips
from app.resources.deploy.uploads import Upload
from app.resources.deploy.deployed_ips import Deployed_ips
from app.resources.deploy.checkfile import Checkfile
from app.resources.deploy.cpfile import Cpfile
from app.resources.deploy.rmfile import Rmfile
from app.resources.deploy.appips import App_ips

monkey.patch_all()

server = WSGIServer(('0.0.0.0', 5000), app)

api.add_resource(Mysql, '/mysql')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Manage, '/manage')
api.add_resource(Deployips, '/deployips')
api.add_resource(Deployed_ips, '/deployed_ips')
api.add_resource(Upload, '/upload')
api.add_resource(Checkfile, '/checkfile')
api.add_resource(Cpfile, '/cp')
api.add_resource(Rmfile, '/rm')
api.add_resource(App_ips, '/app_ips')

if __name__ == '__main__':
    server.serve_forever()
