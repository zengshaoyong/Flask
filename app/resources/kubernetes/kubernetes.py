from kubernetes import client
from kubernetes.client.rest import ApiException
from flask_restful import Resource, reqparse
from app.common.abort import generate_response
from flask_login import login_required
from config import APP_ENV, configs
from flask_login import current_user
from app.common.auth import query_user, query_ldap_user
import yaml
import os

basedir = os.getcwd()
file_dir = os.path.join(basedir, 'upload')


class Kubernetes(Resource):
    decorators = [login_required]

    def __init__(self):
        self.Token = configs[APP_ENV].kubernetes_Token
        self.APISERVER = configs[APP_ENV].kubernetes_APISERVER
        configuration = client.Configuration()
        configuration.host = self.APISERVER
        # configuration.verify_ssl = False
        configuration.verify_ssl = True
        configuration.ssl_ca_cert = "ca.pem"
        configuration.api_key = {"authorization": "Bearer " + self.Token}
        client.Configuration.set_default(configuration)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('task', type=str, location='args')
        self.parser.add_argument('name', type=str, location='args')
        self.parser.add_argument('ns_name', type=str, location='args')
        self.parser.add_argument('container_name', type=str, location='args')
        self.parser.add_argument('image', type=str, location='args')
        self.parser.add_argument('yaml', type=str, location='args')
        self.args = self.parser.parse_args()

    def get(self):
        core = client.CoreV1Api()
        apps = client.AppsV1Api()
        extension = client.NetworkingV1beta1Api()
        if (current_user.type == 'account'):
            namespace = query_user(current_user.id).namespace
        elif (current_user.type == 'ldap'):
            namespace = query_ldap_user(current_user.id).namespace
        task = self.args['task']
        name = self.args['name']
        yaml_file = self.args['yaml']
        container_name = self.args['container_name']
        image = self.args['image']
        if task == 'getns':
            ret = core.list_namespace()
            res = []
            if ret.items != '':
                for i in ret.items:
                    res.append(i.metadata.name)
                return generate_response(res)
        elif task == 'getpod':
            ret = core.list_namespaced_pod(namespace=namespace)
            res = []
            n = 1
            if ret.items != '':
                for i in ret.items:
                    # print(i)
                    data = {
                        'key': n,
                        'name': i.metadata.name, 'namespace': i.metadata.namespace,
                        'status': i.status.phase,
                        'container_statuses': i.status.container_statuses[0].state.waiting,
                        'pod_ip': i.status.pod_ip,
                        'host_ip': i.status.host_ip,
                        'ready': i.status.container_statuses[0].ready,
                        'restart_count': i.status.container_statuses[0].restart_count
                    }
                    res.append(data)
                    n = n + 1
                return generate_response(res)
        elif task == 'getsvc':
            ret = core.list_namespaced_service(namespace=namespace)
            res = []
            n = 1
            if ret.items != '':
                for i in ret.items:
                    data = {
                        'key': n,
                        'name': i.metadata.name,
                        'namespace': i.metadata.namespace,
                        'cluster_ip': i.spec.cluster_ip,
                        'selector': i.spec.selector
                    }
                    res.append(data)
                    n = n + 1
                return generate_response(res)
        elif task == 'getpvc':
            ret = core.list_namespaced_persistent_volume_claim(namespace=namespace)
            res = []
            n = 1
            if ret.items != '':
                for i in ret.items:
                    data = {
                        'key': n,
                        'name': i.metadata.name,
                        'namespace': i.metadata.namespace,
                        'access_modes': i.spec.access_modes[0],
                        'capacity': i.status.capacity,
                        'phase': i.status.phase
                    }
                    res.append(data)
                    n = n + 1
                return generate_response(res)
        elif task == 'getdm':
            ret = apps.list_namespaced_deployment(namespace=namespace)
            res = []
            n = 1
            if ret.items != '':
                for i in ret.items:
                    # print(i)
                    data = {
                        'key': n,
                        'name': i.metadata.name,
                        'namespace': i.metadata.namespace,
                        'image': i.spec.template.spec.containers[0].image,
                        'container_name': i.spec.template.spec.containers[0].name,
                    }
                    res.append(data)
                    n = n + 1
            return generate_response(res)
        elif task == 'geting':
            ret = extension.list_namespaced_ingress(namespace=namespace)
            res = []
            n = 1
            if ret.items != '':
                for i in ret.items:
                    # print(i)
                    data = {
                        'key': n,
                        'name': i.metadata.name,
                        'namespace': i.metadata.namespace,
                        'host': i.spec.rules[0].host,
                        'backend_svc': i.spec.rules[0].http.paths[0].backend.service_name,
                    }
                    res.append(data)
                    n = n + 1
            return generate_response(res)
        elif task == 'deletepod':
            try:
                core.delete_namespaced_pod(name=name, namespace=namespace)
                return generate_response('删除成功')
            except ApiException as e:
                return generate_response("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e.reason)
        elif task == 'deletedm':
            try:
                apps.delete_namespaced_deployment(name=name, namespace=namespace)
                return generate_response('删除成功')
            except ApiException as e:
                return generate_response(
                    "Exception when calling AppsV1Api->delete_namespaced_deployment: %s\n" % e.reason)
        elif task == 'editdm':
            body = {'kind': 'Deployment',
                    'spec': {'template': {'spec': {'containers': [{'image': image, 'name': container_name, }]}, }, },
                    'apiVersion': 'apps/v1', 'metadata': {'name': name}}
            try:
                apps.patch_namespaced_deployment(name=name, namespace=namespace, body=body)
                return generate_response('修改成功')
            except ApiException as e:
                return generate_response(
                    "Exception when calling AppsV1Api->patch_namespaced_deployment: %s\n" % e.reason)
        elif task == 'createdm':
            yaml_dir = os.path.join(file_dir, yaml_file)
            with open(yaml_dir, 'r') as f:
                body = yaml.safe_load(f.read())
            # print(body)
            try:
                apps.create_namespaced_deployment(namespace=namespace, body=body)
                return generate_response('创建成功')
            except ApiException as e:
                return generate_response(
                    "Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e)
        # elif task == 'reading':
        #     ret = extension.read_namespaced_ingress(name=name, namespace=namespace)
        #     print(ret)
