# filename: config.py
APP_ENV = "test"


class BaseConfig:
    DEBUG = False


class Development(BaseConfig):
    kubernetes_Token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IlgtSVBYUENiNjNSUFVaU3FBRUhpNkdDNE9hUnl6Y25fRzNuNUpDS2VsRUEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tdm05a3YiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiOThhMDRjOTgtOGVlOS00ZDA1LThjYzUtYTM5MGZmOTYxZDU4Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmVybmV0ZXMtZGFzaGJvYXJkOmRhc2hib2FyZC1hZG1pbiJ9.pEfSnR2AQzRz2qY1ObchVVXxeKF1MTCjVteutBWpYsv_z-TtRJp4IUhtpoPEgYE3kOZPzScBiCjzkvvBBatb45lkiyog2Zu4xcc0NzwSH1BwRg36X_MGFFCHFXYukDCYPliZzfdxBnJej3xmgnCkY3TVPubKeyYqmV2-1ltkJkyh_YYohyDqTOkO3XctRpU0suPtyjMvdQJb4BqDhfs6I3cuJ5EDz8PdrdDn2BfwzwrHghPwMs4C62XBnw4woDf6pbrQTXIz0jbfJ2Nk9x7wylOf6HfYgscdZv-FMn0PT2TpfVafJsBfM1ywPWdenqS0ykqpuWAgizmzKg6QzM9Z6w'
    kubernetes_APISERVER = 'https://192.168.197.210:6443'


class Test(BaseConfig):
    host = 'localhost'
    port = '3306'
    database = 'mysql'
    user = 'root'
    password = '123456'
    charset = 'utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/cmdb'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/cmdb'
    SECRET_KEY = 'How do you turn this on'
    kubernetes_Token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tOXRjeDIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiOThiZWU2MGYtNjkwOC00MWQ2LThhYWEtNTQ2YWE1YWQ3ZTg2Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.TkycC14sShHenYXtK6VhhlbQjU_Ox9DWomnpkZ9CWuT4HaLA1PDO8RD7m4rBWPQjkdpXzABV1vqaEEbV5_4HX75xn4S6KBV7J-8SdbwMQKMLMlrRVTK9hggH-Lo4Fn2A8Nl1c6er0uDNNChruq-pA86PAwZ03XWI9Pn4NryN9420bX5Z76uo6bt_o15x_sG0R3Nn-Qv22aFHBsODtlgXfvAGpZpXu0kSCKWR0he9WF_DJ0iVHfH8OJEfuZR_YHi75QPsb_j0fRLkKiJ6SbqAttpU26IZMPG3ZRXtMPcGso-76pJY1pZdo-cb0PKrqx25wiBvBAT6q0XEDBWoE4y0kg'
    kubernetes_APISERVER = 'https://119.23.149.192:6443'
    # kubernetes_APISERVER = 'http://119.23.149.192:8443'


class Product(BaseConfig):
    host = '127.0.0.1'
    port = '3305'
    database = 'mysql'
    user = 'cmdb'
    password = '123456789'
    charset = 'utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql://cmdb:123456789@127.0.0.1:3305/cmdb'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/cmdb'
    SECRET_KEY = 'How do you turn this on'
    kubernetes_Token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tOXRjeDIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiOThiZWU2MGYtNjkwOC00MWQ2LThhYWEtNTQ2YWE1YWQ3ZTg2Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.TkycC14sShHenYXtK6VhhlbQjU_Ox9DWomnpkZ9CWuT4HaLA1PDO8RD7m4rBWPQjkdpXzABV1vqaEEbV5_4HX75xn4S6KBV7J-8SdbwMQKMLMlrRVTK9hggH-Lo4Fn2A8Nl1c6er0uDNNChruq-pA86PAwZ03XWI9Pn4NryN9420bX5Z76uo6bt_o15x_sG0R3Nn-Qv22aFHBsODtlgXfvAGpZpXu0kSCKWR0he9WF_DJ0iVHfH8OJEfuZR_YHi75QPsb_j0fRLkKiJ6SbqAttpU26IZMPG3ZRXtMPcGso-76pJY1pZdo-cb0PKrqx25wiBvBAT6q0XEDBWoE4y0kg'
    kubernetes_APISERVER = 'https://119.23.149.192:6443'
    # kubernetes_APISERVER = 'http://119.23.149.192:8443'


configs = {
    'dev': Development,
    'test': Test,
    'pro': Product,
}
