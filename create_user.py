from app.models.db import Userinfo, LdapUser
from app import db
from werkzeug.security import check_password_hash

# test = Userinfo.query.filter(Userinfo.username == 'test').first()
# print(test.check_password('123456789'))

test = LdapUser.query.filter(LdapUser.username == 'zengshaoyong').first()
print(test.__dict__)

#
# test = Userinfo(username='multi', password='123456789', currentAuthority='admin, user', namespace='kube-system')
# db.session.add(test)
# db.session.commit()

# print(check_password_hash(test.password, '123456789'))
