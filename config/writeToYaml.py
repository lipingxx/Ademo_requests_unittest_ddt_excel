#!/usr/bin/python3
# -*- coding:utf-8 -*-

import yaml
import os

cur_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(cur_path,'confyaml.yaml')

# 写入yaml 文件,a->追加写入，w->覆盖写入
fw = open(yaml_path,'a',encoding='utf-8')
# 构建数据
data = {
    "cookie1":{'domain': '.haha', 'expiry': 111111, 'httpOnly': False,
               'name': '_ui_', 'path': '/', 'secure': False, 'value': 'value'}
        }
# 装载数据
yaml.dump(data,fw)
# 读取数据，获取文件
f = open(yaml_path,'r',encoding='utf-8')
# 读取文件
content = f.read()
# 加载数据
x = yaml.load(content)
# 打印读取写入的数据
print(x.get("cookie1"))