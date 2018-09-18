#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
    第一步：加载测试用例（全部加载，或者添加一行，根据“Y”or"No"来决定是否执行）
    第二步：执行测试用例
    第三步：获取最新的测试报告（logging、report+time、testresult）
    第四步：邮件发送
'''
import unittest
import os
import HTMLTestRunner
from Ademo_unittest_logging_email_test.common import HTMLTestRunner_api
from Ademo_unittest_logging_email_test.common import sendEmail
from Ademo_unittest_logging_email_test.common import create_find_report

# 获取当前路径
cur_path = os.path.dirname(os.path.relpath(__file__))

def add_case(caseName='case',rule='test*.py'):
    '''第一步：加载测试用例'''
    # 获取用例文件夹,如果不存在这个case文件夹，就会自动创建一个
    case_path = os.path.join(cur_path,caseName)
    if not os.path.exists(case_path):
        os.mkdir(case_path)

    # 加载case文件夹下的所有测试用例
    discover = unittest.defaultTestLoader.discover(case_path,
                                                   pattern=rule,
                                                   top_level_dir=None)
    print(discover)
    return discover

def run_case(allCase,newFile):
    '''
    #第二步：执行测试用例，并生成按时间排序的测试报告
            参数：allCase 代表所有加载的测试用例
    '''
    report_abspath = newFile + r'\result.html'
    print("测试报告生成地址：%s"%report_abspath)
    fp = open(report_abspath,"wb")
    # 创建HTMLRunner的类对象runner
    #runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
    runner = HTMLTestRunner_api.HTMLTestRunner(stream=fp,
                                           verbosity=2,
                                           title=u'自动化测试执行报告',
                                           description=u'用例执行情况')
    # 执行方法run()
    runner.run(allCase)
    fp.close()

if __name__ == "__main__":
    # step one : 获取测试用例
    all_case = add_case()

    # step two : 创建此次日志文件夹，执行测试用例
    target = create_find_report.ReportFile()
    new_logfile = target.create_logFile()
    run_case(all_case,new_logfile)

    # step three : 获取report文件夹下最新的测试报告文件
    newest_HTMLreport = target.get_lastestHTMLReport()
    print("newestHTMLreport:",newest_HTMLreport)

    # step four : 邮箱配置，并发送邮件
    from Ademo_unittest_logging_email_test.config import readConfig
    mail_smtpserver = readConfig.get_smtpServer('smtp_server')
    mail_port = readConfig.get_port('port')
    mail_sender = readConfig.get_sender('sender')
    mail_pwd = readConfig.get_pwd('pwd')
    mail_receiverList_tmp = readConfig.get_receiver('receiver')     # 返回str类型，需要转换为list
    mail_receiverList = mail_receiverList_tmp.split(',')            # 以“,”进行切分，返回list
    print("收件人：",mail_receiverList)
    mail_subject = readConfig.get_subject('subject')

    # 发送邮件,smtpServer, mailPort, mailSender, mailPwd, mailtoList, mailSubject
    s = sendEmail.SendEmail(mail_smtpserver, mail_port, mail_sender, mail_pwd, mail_receiverList, mail_subject)
    s.sendFile(newest_HTMLreport)
    print("main send end !")