from app.models.db import Userinfo
from app import db
from werkzeug.security import check_password_hash

test = Userinfo.query.filter(Userinfo.username == 'test').first()
print(test.check_password('123456789'))


# test = Userinfo(username='test', password='123456789')
# db.session.add(test)
# db.session.commit()


# print(check_password_hash(test.password, '123456789'))




