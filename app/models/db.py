from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Userinfo(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), nullable=False)
    currentAuthority = db.Column(db.String(255), nullable=False)
    namespace = db.Column(db.String(255))
    group = db.Column(db.String(255), nullable=False)
    instances = db.Column(db.String(255))

    def __init__(self, username, password, currentAuthority, namespace, group, instances):
        self.username = username
        self.password = generate_password_hash(password)
        self.currentAuthority = currentAuthority
        self.namespace = namespace
        self.group = group
        self.instances = instances

        # 定义一个验证密码的方法

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)


class LdapUser(db.Model):
    __tablename__ = 'ldap_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    currentAuthority = db.Column(db.String(255), nullable=False)
    namespace = db.Column(db.String(255))
    group = db.Column(db.String(255), nullable=False)
    instances = db.Column(db.String(255))

    def __init__(self, username, currentAuthority, namespace, group, instances):
        self.username = username
        self.currentAuthority = currentAuthority
        self.namespace = namespace
        self.group = group
        self.instances = instances


class database_info(db.Model):
    __tablename__ = 'instances'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(255), nullable=False)
    port = db.Column(db.String(255), nullable=False)
    read_user = db.Column(db.String(255), nullable=False)
    read_password = db.Column(db.String(255), nullable=False)
    execute_user = db.Column(db.String(255), nullable=False)
    execute_password = db.Column(db.String(255), nullable=False)
    instance = db.Column(db.String(255), nullable=False)

    def __init__(self, instance, ip, port, read_user, read_password, execute_user, execute_password):
        self.instance = instance
        self.ip = ip
        self.port = port
        self.read_user = read_user
        self.read_password = read_password
        self.execute_user = execute_user
        self.execute_password = execute_password


db.create_all()
