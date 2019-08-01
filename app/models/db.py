from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Userinfo(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    # 定义一个验证密码的方法
    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)


class Ipaddrs(db.Model):
    __tablename__ = 'ipaddrs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    ips = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(80), nullable=False)

    def __init__(self, name, ips):
        self.name = name
        self.ips = ips
        self.type = type

    def __repr__(self):
        return '<name %r>' % self.name

    def query_ips(self):
        return self.ips

    def query_type(self):
        return self.type

    @staticmethod
    def add_app(name, ips):
        new = Ipaddrs(name=name, ips=ips, type=type)
        db.session.add(new)
        db.session.commit()

    def delete_app(self, name):
        db.session.delete(name)
        db.session.commit()

    def update_app(self, ips):
        self.ips = ips
        db.session.commit()


# db.create_all()