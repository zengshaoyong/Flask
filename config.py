# filename: config.py
APP_ENV = "test"


class BaseConfig:
    DEBUG = False


class Development(BaseConfig):
    CRP_URL = 'xxxx'
    ...


class Test(BaseConfig):
    host = 'localhost'
    port = '3306'
    database = 'mysql'
    user = 'root'
    password = '123456'
    charset = 'utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/flask'
    SECRET_KEY = 'How do you turn this on'


class Product(BaseConfig):
    CRP_URL = 'xxxx'
    ...


configs = {
    'dev': Development,
    'test': Test,
    'pro': Product,
}
