from jira import JIRA
from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox, HTMLBody
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
# cred = Credentials(r'WDPH\zengshaoyong', 'Asdfgzxcvb.123')
# config = Configuration(server='https://owa.wanda.cn/owa', credentials=cred, auth_type=NTLM)
# a = Account(
#     primary_smtp_address='zengshaoyong@wanda.cn', config=config, autodiscover=True
# )
# print('1.邮箱连接成功')

def Email(to, subject, body):
    creds = Credentials(
        username='xxx',
        password='xxx'
    )
    account = Account(
        primary_smtp_address='xxx@wanda.cn',
        credentials=creds,
        autodiscover=True,
        access_type=DELEGATE
    )
    m = Message(
        account=account,
        subject=subject,
        body=HTMLBody(body),
        to_recipients=[Mailbox(email_address=to)]
    )
    m.send()


def Smtp(to, subject, content):
    mail_host = "mail.wanda.com.cn"
    mail_user = "wdph_robot"
    mail_pass = "y21zlepj"
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("JIRA", 'utf-8')
    message['To'] = Header(to, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj.sendmail("wdph_robot@wanda.com.cn", to, message.as_string())


options = {
    'server': 'http://10.53.144.208:8080'}
jira = JIRA(options, basic_auth=('admin', 'wanda@2017'))

# Get all projects viewable by anonymous users.
# projects = jira.projects()

# Sort available project keys, then return the second, third, and fourth keys.
# keys = sorted([project.key for project in projects])

# Get an issue.
# issue = jira.issue('YWXT-2099')
# content = issue.fields.description
# if content == None:
#     content = issue.fields.attachment[0]
# print(content)
issues_in_proj = jira.search_issues('project=YWXT')
# oh_crap = jira.search_issues('assignee = currentUser() and due < endOfWeek() order by priority desc', maxResults=5)


# atl_comments = issue.fields.assignee
# watcher = jira.watchers(issue)
# # summary = issue.fields.summary
# print(watcher.watchers)
# print(atl_comments.name)

for i in issues_in_proj:
    issue = jira.issue(i)
    user = issue.fields.assignee
    watcher = jira.watchers(issue)
    # print(issue.fields.__dict__)
    # for watcher in watcher.watchers:
    if user:
        if user.name == 'jiangbinbin5' or user.name == 'xiaqiang1' or user.name == 'zhengyifei3' or user.name == 'chenguangzhao' or user.name == 'zengshaoyong' \
                or user.name == 'liaowenqi' or user.name == 'sunyufei8' or user.name == 'lizhuolin3':
            subject = '%s 提出 %s 单' % (watcher.watchers[0], issue)
            content = issue.fields.description
            if content == None:
                content = '请查看附件'
            email = user.emailAddress
            print(user)
            print(user.emailAddress)
            print(issue)
            print(content)
# Email(email, subject, content)
# Smtp(email, subject, content)
