#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''
    介绍如何使用python进行各种类型附件的发送

    Python发送一个未知MIME类型的文件附件基本思路：
    0、前提：导入邮件发送模块
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            import smtplib
    1、构造MIMEMultipart对象作为根容器
    2、构造MIMEText对象作为邮件显示内容并附加到根容器
    3、构造MIMEBase对象作为文件附件内容并附加到跟容器
        a、读入文件内容并格式化
        b、设置附件头
    4、设置根容器属性
    5、得到格式化后的完整文本
    6、用smtp发送邮件
    封装成Email类。
'''
# 20180803 需要添加发送压缩文件；需要考虑如何添加邮件正文部分。

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

class SendEmail(object):
    '''
    发送邮件模块封装，属性均从config.ini文件获得
    '''
    def __init__(self, smtpServer, mailPort, mailSender, mailPwd, mailtoList, mailSubject):  # ,mailContent):
        self.mail_smtpserver = smtpServer
        self.mail_port = mailPort
        self.mail_sender = mailSender
        self.mail_pwd = mailPwd
        # 接收邮件列表
        self.mail_receiverList = mailtoList
        self.mail_subject = mailSubject
        # self.mail_content = mailContent

    def sendFile(self, reportFile):
        '''
        发送各种类型的附件
        '''

        # 构建根容器
        msg = MIMEMultipart()
        # MIMEText -> def __init__(self, _text, _subtype='plain', _charset=None, *, policy=None)
        # 邮件正文部分body，1、可以用HTML自己自定义body内容；2、读取其他文件的内容为body
        # body = "您好，<p>这里是使用Python登录邮箱，并发送附件的测试<\p>"
        with open(reportFile,'r',encoding='UTF-8') as f:
            body = f.read()

        msg.attach(MIMEText(_text=body, _subtype='html', _charset='utf-8'))  # _charset 是指Content_type的类型

        # 邮件主题、发送人、收件人、内容
        msg['Subject'] = self.mail_subject  # u'自动化测试报告'
        msg['from'] = self.mail_sender
        msg['to'] = self.mail_pwd

        # 添加附件
        attachment = MIMEText(_text=open(reportFile, 'rb').read(), _subtype='base64',_charset= 'utf-8')
        attachment['Content-Type'] = 'application/octet-stream'
        attachment['Content-Disposition'] = 'attachment;filename = "result.html"'
        msg.attach(attachment)

        try:
            smtp = smtplib.SMTP_SSL(host=self.mail_smtpserver, port=self.mail_port)  # 继承自SMTP
        except:
            smtp = smtplib.SMTP()
            smtp.connect(self.mail_smtpserver, self.mail_port)

        # smtp.set_debuglevel(1)
        smtp.starttls()     # Puts the connection to the SMTP server into TLS mode.
        # 用户名和密码
        smtp.login(user=self.mail_sender, password=self.mail_pwd)

        # def sendmail(self, from_addr, to_addrs, msg, mail_options=[],rcpt_options=[]):
        smtp.sendmail(self.mail_sender, self.mail_receiverList, msg.as_string())
        smtp.quit()


    def sendZipFile(self, ZipFile):
        '''
        发送压缩文件
        '''
        pass

if __name__ == "__main__":
    mail_smtpserver = 'smtp.qq.com'
    mail_port = 587
    mail_sender = '2445425105@qq.com'
    mail_pwd = 'ruuzsciabmzkdhif'  # 抛出int***错误，加上引号
    mail_receiverList = ['2445425105@qq.com', 'xiongliping@cefcfco.com']
    mail_subject = u'自动化测试报告'
    s = SendEmail(mail_smtpserver, mail_port, mail_sender, mail_pwd, mail_receiverList, mail_subject)
    s.sendFile('F:\Python_project\PythonLearnning_2018\send_email\sendEmail_Test.html.tar.gz')
    print('--- test end --- ')
    # 抛错：smtplib.SMTPAuthenticationError: (535, b'Error: \xc7\xeb\xca\xb9\xd3\xc3\xca\xda\xc8\xa8\xc2\xeb\xb5\xc7\xc2\xbc\xa1\xa3\xcf\xea\xc7\xe9\xc7\xeb\xbf\xb4: http://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256')
    # 点击最后的链接，其实是因为授权码问题，替换成uikxucdtqipbecja
    # 替换授权码后继续报错，535   --> 替换端口
    # qq邮箱ssl协议端口  465/587
    # then，报错：smtplib.SMTPAuthenticationError: (530, b'Must issue a STARTTLS command first.')
    # 解决方法：在login()之前，添加一句：smtp.starttls()
