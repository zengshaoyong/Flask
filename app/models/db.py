from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, TIMESTAMP, text


class Userinfo(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), nullable=False)
    currentAuthority = db.Column(db.String(255), nullable=False)
    namespace = db.Column(db.String(255))
    group = db.Column(db.String(255), nullable=False)
    execute_instances = db.Column(db.String(255))
    read_instances = db.Column(db.String(255))

    def __init__(self, username, password, currentAuthority, namespace, group, execute_instances, read_instances):
        self.username = username
        self.password = generate_password_hash(password)
        self.currentAuthority = currentAuthority
        self.namespace = namespace
        self.group = group
        self.execute_instances = execute_instances
        self.read_instances = read_instances

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
    execute_instances = db.Column(db.String(255))
    read_instances = db.Column(db.String(255))
    redis = db.Column(db.String(255))

    def __init__(self, username, currentAuthority, namespace, group, execute_instances, read_instances):
        self.username = username
        self.currentAuthority = currentAuthority
        self.namespace = namespace
        self.group = group
        self.execute_instances = execute_instances
        self.read_instances = read_instances


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


class record_sql(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), nullable=False)
    instance = db.Column(db.String(255), nullable=False)
    time = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'),
                     server_onupdate=text('CURRENT_TIMESTAMP'))
    sql = db.Column(db.String(255), nullable=False)

    def __init__(self, user, sql, instance):
        self.user = user
        self.sql = sql
        self.instance = instance


db.create_all()
