#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''
    获取接口api数据
    通过readConfig得到testOrder.xlsx
    根据list中的case_path、which、runTag来决定是否决定执行该条用例

# ddt语法（data-driven tests）
    # 包含：类装饰器ddt，两个方法装饰器data、file_data
    # 通常情况下，data中的数据按照一个参数传递给测试用例。如果data中含有多个数据，以元、列表、字典等数据进行处理。
    # @date(a,b) - a和b各运行一次；
    # @date([a,b],[c,d])   (另一行)@unpack
    # @file_data(filename)
'''

import unittest
import os,time,ddt
import xlrd
from Ademo_unittest_logging_email_test.config import readConfig
from Ademo_unittest_logging_email_test.common import requestsModule
from Ademo_unittest_logging_email_test.common import read_excel
from Ademo_unittest_logging_email_test.common import write_excel
from Ademo_unittest_logging_email_test.common import create_find_report
from Ademo_unittest_logging_email_test.common import logger

curpath = os.path.dirname(os.path.realpath(__file__))

# 接口数据用例存放文件夹，可以用config进行配置
data_path = readConfig.get_excelPath("excelPath")

# 具体哪个接口文档
excel_name = readConfig.get_excelName("excelName")

t = read_excel.ApiDefine_change(data_path)
testdata = t.dict_data()

target_file = create_find_report.ReportFile()
# *要在main中先创建新的文件夹，不然copy的excel会进到上一次执行生成的测试报告集中
base_path = target_file.get_lastestReportFile()
# get:拷贝后，excel所在的路径
reportxlsx = os.path.join(base_path,excel_name)
output = base_path + '\\响应text.txt'

@ddt.ddt
class Test_api(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''
            准备工作
            找当前报告路径下最新的报告文件夹，
            将要执行的测试用例xlsx文档拷贝至report文件夹
        '''
        # 如果有登录的话，就在这里先登录
        # cls.s = requests.session()
        write_excel.copy_excel(data_path, reportxlsx)  # 复制xlsx


    @ddt.data(*testdata)
    def test_api(self,data):
        log_path = open(output, 'a+')
        print('==============================================================',file=log_path)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), file=log_path)

        res = requestsModule.send_requests(data)
        requestsModule.wirte_result(res, filename=reportxlsx)

        # 检查点 checkpoint
        check = data["checkpoint"].strip()
        print("检查点->：%s" % check)
        # 返回结果
        res_text = res["text"]
        print("返回实际结果->：%s" % res_text)
        # 断言不要随便乱用
        #Tag = self.assertTrue(check in res_text)
        if  check in res_text:
            print('第 %s 条测试用例 - Pass'%data['id'],file=log_path)
            print(res_text, '\n', file=log_path)
        else:
            print('第 %s 条测试用例 - Fail' % data['id'],file=log_path)

        # 运行结束后，记得关闭文件
        log_path.close()

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()