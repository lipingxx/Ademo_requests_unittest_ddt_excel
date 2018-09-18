#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os,time
import unittest
import requests
from Ademo_unittest_logging_email_test.common import logger

class RMSTest01(unittest.TestCase):
    ''''''
    log = logger.Log()

    def login(self, username, psw, reme=True):
        '''三个参数：
        账号：username，密码：psw,记住登录：reme=True'''
        url = "https://passport.cnblogs.com/user/signin"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
            "Cookie": "这里是抓包后获取的cookies",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Content-Length": "385"
                 }
        json_data = {"input1": username,
                    "input2": psw,
                    "remember": reme}

        res = requests.post(url, headers=header, json=json_data, verify=False)
        result1 = res.content  # 字节输出
        self.log.info("博客园登录结果：%s"%result1)
        return res.json()      # 返回json

    def test_login1(self):
        u'''测试登录：正确账号，正确密码'''
        self.log.info("------登录成功用例：start!---------")
        username = "这里是抓包后获取的博客园的加密账号",
        self.log.info("输入正确账号：%s" % username)
        psw = "这里是抓包后获取的博客园的加密密码",
        self.log.info("输入正确密码：%s" % psw)
        result = self.login(username, psw)
        self.log.info("获取测试结果：%s" % result)
        self.assertEqual(result["success"], True)
        self.log.info("------pass!---------")

if __name__ == "__main__":
    unittest.main(verbosity=2)