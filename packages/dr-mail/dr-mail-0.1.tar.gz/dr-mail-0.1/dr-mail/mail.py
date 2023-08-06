import json
import smtplib

from email.header import Header
from email.mime.text import MIMEText
from email import encoders
from email.utils import parseaddr, formataddr


class config_test:
    """fulfill this for complete the mail server configuration."""
    def __init__(self, mail_host, mail_user, mail_passwd, sender):

        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_passwd = mail_passwd
        self.sender = sender


def send_mail(receivers: list, text: str, sender_title: str, subject: str, mail_serv):
    mail_host = mail_serv.mail_host
    mail_user = mail_serv.mail_user
    mail_passwd = mail_serv.mail_passwd
    sender = mail_serv.sender


    for i in range(len(receivers)):
        message = MIMEText(text, 'plain', 'utf-8')
        message['From'] = formataddr((sender_title, sender), charset='utf-8')
        message['To'] = formataddr((receivers[i]['name'], receivers[i]['address']), charset='utf-8')
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            smtpObj.login(mail_user, mail_passwd)
            smtpObj.sendmail(sender, receivers[i]['address'], message.as_string())
            print('邮件发送成功')
        except smtplib.SMTPException:
            print('无法发送邮件')

def build_receivers_dict(addresses: list, names: list) -> dict:
    list = []
    for i in range(len(addresses)):
        dict = {}
        dict['address'] = addresses[i]
        dict["name"] = names[i]
        list.append(dict)

    return list
