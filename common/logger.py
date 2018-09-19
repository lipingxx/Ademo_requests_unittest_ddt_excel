#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
    print()可以实现在控制台打印想看的信息
    但是当我们需要看大量的地方或者在一个文件中查看所有的打印信息时，print()就不太方便了。
    引入学习Python的logging模块。
    可以更好地控制在哪个地方输出信息，怎么输出，信息的级别，日志存放路径。
    一、消息级别
    debug、info、warning、error、critical;
    debug:打印全部的、详细的日志信息，通常出现在诊断问题时。
    info:打印各级别的日志，确认一切按预期运行；
    warning:打印warning、error、critical级别的日志；
    error:打印error、critical级别的日志；
    critical：打印critical级别的日志；
    二、
'''

import os
import time
import logging

# 获取上一层目录
cur_upPath = os.path.abspath(os.path.dirname(os.getcwd()))
#print(cur_upPath)
# cur_path = os.path.dirname(os.path.relpath(__file__))
# 存放日志的路径
#log_path = os.path.join(os.path.join(cur_path),'logs')
log_path = os.path.join(cur_upPath,'logs')
# 如果不存在该路径，则先创建一个
if not os.path.exists(log_path):
    os.mkdir(log_path)

class Log(object):
    ''''''
    def __init__(self):
        # log文件名
        self.log_name = os.path.join(log_path,'%s.log'%time.strftime('%Y%m%d.%H.%M.%S'))
        self.logger = logging.getLogger()
        # 设置日志级别
        self.logger.setLevel(logging.DEBUG)
        # log输出格式：logging.Formatter()
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    # private，内部逻辑进行隐藏，代码封装
    def __console(self,level,message):
        '''写日志'''

        # FileHandler : 写日志到本地
        fh = logging.FileHandler(self.log_name,'a',encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        # 添加一个Handler
        self.logger.addHandler(fh)

        # StreamHandler : 写日志到控制台
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(self.formatter)
        self.logger.addHandler(sh)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)

        # 移除handler，以避免重复输出
        self.logger.removeHandler(sh)
        self.logger.removeHandler(fh)

        fh.close()

    # 调用不同级别的方法时，不用关心内部__console()的实现
    def debug(self,message):
        self.__console('debug',message)

    def info(self,message):
        self.__console('info',message)

    def warning(self,message):
        self.__console('warning',message)

    def error(self,message):
        self.__console('error',message)

log = Log()

from functools import wraps
def deco_logger(param):
    def wrap(function):
        @wraps(function)
        def _wraps(*args,**kwargs):
            log.info('当前运行的模块为：{}'.format(param))
            log.info('当前函数args参数列表为{}'.format(str(args)))
            log.info('当前函数kwargs参数列表为{}'.format(str(kwargs)))
            return function(*args,**kwargs)
        return _wraps
    return wrap

# test
@deco_logger('logger.py测试开始')   # 装饰器本身带参数
def test():
    log.info('log.info')
    log.error(' --- bug appearance --- ')
    log.warning(' ---- warnning:test end --- ')

if __name__ == "__main__":
    print('测试用')
    test()

'''
if __name__ == "__main__":
    log = Log()
    log.info(' ---- test begin --- ')
    log.info(' ---- step 1/2/3 --- ')
    log.error(' --- bug appearance --- ')
    log.warning(' ---- warnning:test end --- ')
'''