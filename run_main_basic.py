#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
    第一步：加载测试用例（全部加载，或者添加一行，根据“Y”or"No"来决定是否执行）
    第二步：执行测试用例
    第三步：获取最新的测试报告（logging、report+time、testresult）
    第四步：邮件发送
'''
import unittest
import os,time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import HTMLTestRunner

# 获取当前路径
cur_path = os.path.dirname(os.path.relpath(__file__))

def add_case(caseName='case',rule='test*.py'):
    '''第一步：加载测试用例'''
    # 获取用例文件夹
    case_path = os.path.join(cur_path,caseName)
    # 如果不存在这个case文件夹，就会自动创建一个
    if not os.path.exists(case_path):
        os.mkdir(case_path)
    # 加载case文件夹下的所有测试用例
    discover = unittest.defaultTestLoader.discover(case_path,
                                                   pattern=rule,
                                                   top_level_dir=None)
    print(discover)
    return discover

# 创建最新报告集合
def create_logFile():
    '''在report文件夹下创建该次执行的报告集合'''
    nowtime = time.strftime("%Y%m%d.%H.%M.%S")
    report_path = os.path.join(cur_path, 'report')
    mkpath = report_path + '\\' + nowtime + ' 测试报告集'
    os.makedirs(mkpath)
    return mkpath

def run_case(allCase):
    '''
    第二步：执行测试用例，并生成按时间排序的测试报告
        参数：allCase 代表所有加载的测试用例
    '''
    # step one:生成最新报告文件夹，以时间进行标记
    now_file = create_logFile()
    # step two:执行测试用例，并生成html测试报告
    report_abspath = now_file + r'\result.html'
    print("测试报告生成地址：%s"%report_abspath)
    fp = open(report_abspath,"wb")
    # 创建HTMLRunner的类对象runner
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           verbosity=2,
                                           title=u'自动化测试执行报告',
                                           description=u'用例执行情况')
    # 执行方法run()
    runner.run(allCase)
    fp.close()

def get_lastestReportFile():
    '''
    第三步：获取最新的测试报告
    '''
    base_reportPath = os.path.join(cur_path,'report')
    all_files = os.listdir(base_reportPath)
    all_files.sort(key=lambda fn:os.path.getmtime(base_reportPath+'\\'+fn) if not os.path.isdir(base_reportPath+'\\'+fn)
                                                                            else 0)
    # get最新文件夹路径，并返回
    latest_FilePath = base_reportPath + '\\' + all_files[-1]
    print(latest_FilePath)
    return latest_FilePath

def send_email(sender,pwd,receiver,smtpserver,reportFile,port):
    '''
    第四步：邮件发送最新的测试报告内容，参数读取配置文件
    '''
    # 先读取文件的内容，存入至mail_body
    # 这里是文件夹，so how？
    with open(reportFile,"rb") as f:
        mail_body = f.read()
    # 定义邮件内容
    msg = MIMEMultipart()
    # MIMEText -> def __init__(self, _text, _subtype='plain', _charset=None, *, policy=None)
    body = MIMEText(mail_body,_subtype='html',_charset='utf-8')
    # 邮件主题、发送人、收件人、内容
    msg['Subject']  = u'自动化测试报告'
    msg['from']     = sender
    msg['to']       = pwd
    msg.attach(body)
    # 添加附件
    attachment  = MIMEText(open(reportFile,'rb').read())#,'base64','utf-8')
    attachment['Content-Type'] = 'application/octet-stream'
    attachment['Content-Disposition'] = 'attachment;filename = "result.html"'
    msg.attach(attachment)

    try:
        smtp = smtplib.SMTP_SSL(smtpserver,port)
    except:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver,port)

    # 用户名和密码
    smtp.login(sender,pwd)
    # def sendmail(self, from_addr, to_addrs, msg, mail_options=[],rcpt_options=[]):
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.quit()
    print('test report email has send out ! ')

if __name__ == "__main__":
    # step one : 获取测试用例
    all_case = add_case()
    # step two : 执行测试用例
    run_case(all_case)
    # step three : 获取report文件夹下最新的测试报告
    newest_report = get_lastestReportFile()
    # step four : 邮箱配置，并发送邮件
    from Ademo_unittest_logging_email_test.config import readConfig
    sender = readConfig.get_sender('sender')
    pwd = readConfig.get_pwd('pwd')
    smtp_server = readConfig.get_smtpServer('smtp_server')
    port = readConfig.get_port('port')
    receiver = readConfig.get_receiver('receiver')

    send_email(sender,pwd,receiver,smtp_server,newest_report,port)

# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc9 in position 3: invalid continuation byte








