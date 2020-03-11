from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from app.resources.mysql.execute.query import *
from app.resources.mysql.instance.query import Instance
from app import app, api
from app.common.auth import Login, Logout
from app.resources.kubernetes.kubernetes import Kubernetes
from app.resources.kubernetes.Upload import Upload
from app.resources.current_user.user import Current_user
from app.resources.audit.mysql.audit import Audit
from app.resources.audit.redis.audit import Audit_redis
from app.resources.redis.execute import Redis

api.add_resource(Mysql, '/mysql')
api.add_resource(Instance, '/instance')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Kubernetes, '/k8s')
api.add_resource(Upload, '/upload')
api.add_resource(Current_user, '/currentUser')
api.add_resource(Audit, '/audit')
api.add_resource(Audit_redis, '/audit_redis')
api.add_resource(Redis, '/redis')

if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
    # app.run(host='0.0.0.0')
