from app.models.db import Userinfo,Ipaddrs
from app import db
from werkzeug.security import check_password_hash

# test = Userinfo.query.filter(Userinfo.username == 'test').first()
# print(test.check_password('123456789'))

#
# test = Userinfo(username='test', password='123456789')
# db.session.add(test)
# db.session.commit()


# print(check_password_hash(test.password, '123456789'))


# test = Ipaddrs(name='wandaph-tmk-deploy-pro', ips='10.161.108.211,10.161.108.212')
# db.session.add(test)
# db.session.commit()


from app.models.db import Ipaddrs

app = Ipaddrs.query.filter(Ipaddrs.name == 'acct-pro').first()
print(app.type)



