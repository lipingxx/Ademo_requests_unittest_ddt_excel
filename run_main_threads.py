#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os,time
import unittest
from tomorrow import threads
from BeautifulReport import BeautifulReport
from Ademo_unittest_logging_email_test.common import sendEmail
from Ademo_unittest_logging_email_test.common import create_find_report

# 当前该文件所在目录
curpath = os.path.dirname(os.path.realpath(__file__))

# 查找"report"文件夹路径
report_path = os.path.join(curpath, "report")
if not os.path.exists(report_path):
    os.mkdir(report_path)

# 存放测试用例数据
case_path = os.path.join(curpath, "case_excel")
#case_path = os.path.join(curpath, "case")

def add_case(casepath=case_path, rule="test*.py"):
    '''加载所有的测试用例'''
    discover = unittest.defaultTestLoader.discover(casepath,
                                                  pattern=rule ,)
    return discover

@threads(3)  # threads(n,timeout)
def run_case(testsuite,newFile):
    result = BeautifulReport(testsuite)
    result.report(filename="result.html",description="多线程执行测试用例",log_path=newFile)

if __name__ == "__main__":
    # step one : 先创建报告集,then获取测试用例
    target = create_find_report.ReportFile()
    new_logfile = target.create_logFile()
    all_case = add_case()
    # step two : 创建此次日志文件夹，执行测试用例
    # run_case(all_case, new_logfile)
    for i in all_case:
        run_case(i,new_logfile)
    # step three : 获取report文件夹下最新的测试报告文件夹
    time.sleep(3)
    newest_HTMLreport = target.get_lastestHTMLReport()
    print("newestHTMLreport:", newest_HTMLreport)

    # step four : 邮箱配置，并发送邮件
    from Ademo_unittest_logging_email_test.config import readConfig
    mail_smtpserver = readConfig.get_smtpServer('smtp_server')
    mail_port = readConfig.get_port('port')
    mail_sender = readConfig.get_sender('sender')
    mail_pwd = readConfig.get_pwd('pwd')
    mail_receiverList_tmp = readConfig.get_receiver('receiver')  # 返回str类型，需要转换为list
    mail_receiverList = mail_receiverList_tmp.split(',')  # 以“,”进行切分，返回list
    print("收件人：", mail_receiverList)
    mail_subject = readConfig.get_subject('subject')

    # 发送邮件,smtpServer, mailPort, mailSender, mailPwd, mailtoList, mailSubject
    s = sendEmail.SendEmail(mail_smtpserver, mail_port, mail_sender, mail_pwd, mail_receiverList, mail_subject)
    s.sendFile(newest_HTMLreport)
    print("main test end !")
