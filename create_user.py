from app.models.db import Userinfo, LdapUser, database_info
from app import db
from werkzeug.security import check_password_hash

# test = Userinfo.query.filter(Userinfo.username == 'test').first()
# print(test.check_password('123456789'))

# test = LdapUser.query.filter(LdapUser.username == 'zengshaoyong').first()
# print(test.__dict__)

#
# test = Userinfo(username='test5', password='123456789', currentAuthority='0', namespace='kube-system', group='test',
#                 execute_instances=None, read_instances=None)
# db.session.add(test)
# db.session.commit()

# test = database_info(instance='platform(test)', ip='127.0.0.1', port='3306', read_user='root', read_password='123456',
#                      execute_user='root', execute_password='123456')
# db.session.add(test)
# db.session.commit()

# print(check_password_hash(test.password, '123456789'))

#
# test = database_info(instance='test', ip='127.0.0.1', port='3306', read_user='root', read_password='123456',
#                      execute_user='root', execute_password='123456')
# db.session.add(test)
# db.session.commit()

# test = database_info.query.filter(database_info.group == 'test').first()
# print(test.__dict__)
