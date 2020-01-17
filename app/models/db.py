from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Userinfo(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), nullable=False)
    currentAuthority = db.Column(db.String(255), nullable=False)
    namespace = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password, currentAuthority, namespace, group):
        self.username = username
        self.password = generate_password_hash(password)
        self.currentAuthority = currentAuthority
        self.namespace = namespace
        self.group = group

        # 定义一个验证密码的方法

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)


class LdapUser(db.Model):
    __tablename__ = 'ldap_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    currentAuthority = db.Column(db.String(255), nullable=False)
    namespace = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(255), nullable=False)

    def __init__(self, username, currentAuthority, namespace, group):
        self.username = username
        self.currentAuthority = currentAuthority
        self.namespace = namespace
        self.group = group

# db.create_all()
