#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''
    report相关：
    创建测试报告集
    寻找最新的测试报告集
    寻找最新报告集中的html报告
'''
import os,time

cur_upPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print("cur_upPath:",cur_upPath)

class ReportFile(object):
    def __init__(self):
        pass

    # 创建最新报告集合
    def create_logFile(self):
        '''在report文件夹下创建该次执行的报告集合'''
        nowtime = time.strftime("%Y%m%d.%H.%M.%S")
        report_path = os.path.join(cur_upPath, 'report')
        mkpath = report_path + '\\' + nowtime + ' 测试报告集'
        os.makedirs(mkpath)
        return mkpath

    def get_lastestHTMLReport(self):
        '''
        获取最新的.html测试报告
        '''
        base_reportPath = os.path.join(cur_upPath, 'report')
        all_files = os.listdir(base_reportPath)
        all_files.sort( key=lambda fn: os.path.getmtime(base_reportPath + '\\' + fn)
                        if not os.path.isdir(base_reportPath + '\\' + fn)
                        else 0)

        # get最新文件夹路径，并返回
        latest_FilePath = base_reportPath + '\\' + all_files[-1] + '\\result.html'
        print("get_lastestHTMLreport:",latest_FilePath)
        return latest_FilePath

    def get_lastestReportFile(self):
        '''
        获取最新的测试报告集文件夹
        '''
        base_reportPath = os.path.join(cur_upPath, 'report')
        all_files = os.listdir(base_reportPath)
        all_files.sort(key=lambda fn: os.path.getmtime(base_reportPath + '\\' + fn) if not os.path.isdir(
            base_reportPath + '\\' + fn)
        else 0)
        # get最新文件夹路径，并返回
        latest_FilePath = base_reportPath + '\\' + all_files[-1]
        # print(latest_FilePath)
        return latest_FilePath
