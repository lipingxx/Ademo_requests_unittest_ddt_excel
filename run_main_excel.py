#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os,time
import unittest


from Ademo_unittest_logging_email_test.common import HTMLTestRunner_api
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

def add_case(casepath=case_path, rule="test*.py"):
    '''加载所有的测试用例'''
    discover = unittest.defaultTestLoader.discover(casepath,
                                                   pattern=rule,)
    print(discover)
    return discover

def run_case(all_case,newFile):
    '''执行所有的用例, 并把结果写入测试报告'''
    report_abspath = newFile + r'\result.html'
    #print("测试报告生成地址：%s" % report_abspath)
    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner_api.HTMLTestRunner(stream=fp,
                                               verbosity=2,
                                               title="测试报告",
                                               description="用例执行情况")
    runner.run(all_case)
    # 打开一个文件后，记得close
    fp.close()

if __name__ == "__main__":
    # step one : 先创建报告集
    target = create_find_report.ReportFile()
    new_logfile = target.create_logFile()
    # then 获取测试用例
    all_case = add_case()

    # step two : 创建此次日志文件夹，执行测试用例
    run_case(all_case, new_logfile)
    # step three : 获取report文件夹下最新的测试报告文件夹
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
