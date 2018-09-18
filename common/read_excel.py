#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
    读取excel接口数据
'''
import xlrd

class ApiDefine_change(object):
    def __init__(self,file):
        self.file = file

    def dict_data(self):#,file,which):
        file = self.file
        data = xlrd.open_workbook(file)
        table = data.sheet_by_index(0)
        # 获取总行数
        nrows = table.nrows
        # 获取接口文档第一行的参数名param_name  ['id','case_name', 'method',..., 'msg', 'status_code']
        param_names = table.row_values(0)
        list = []
        # 循环读取excel中每行的值，返回格式 [{'':''},{'':''}] # json格式
        for rownum in range(1, nrows):
            row_value = table.row_values(rownum)
            if row_value:
                app = {}  # dict
                # 循环读取每行中的每列值
                for i in range(len(param_names)):
                    app[param_names[i]] = row_value[i]
                # 将该行的值{'':'','':''}放入到list中
                list.append(app)
        print(list)
        return list

if __name__ == '__main__':
    file  = 'F:\Python_project\Ademo_unittest_logging_email_test\dataExcel\出口合理性分析导出接口new.xlsx'
    # which = 1
    a = ApiDefine_change(file)
    a.dict_data()

