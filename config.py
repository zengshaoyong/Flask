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


class Product(BaseConfig):
    CRP_URL = 'xxxx'
    ...


configs = {
    'dev': Development,
    'test': Test,
    'pro': Product,
}
