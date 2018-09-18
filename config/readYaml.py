#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
    该模块读取yaml文件 封装
'''
_author_ = 'xlp'

import yaml
import os

# 先找到yaml文件的路径
cur_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(cur_path,'confyaml.yaml')

# 打开yaml文件
f = open(yaml_path,'r',encoding='utf-8')
# 读取
yaml_content = f.read()
print(type(yaml_content))       # <class 'str'>
print(yaml_content)             # 注释也读取出来了

# 有没有什么方法转化为其他类型
yaml_content_dict = yaml.load(yaml_content)
print(type(yaml_content_dict))
print("yaml_content_dict:",yaml_content_dict)            # but,注释的地方会报错？一个yaml文件只允许存放一种数字类型？？？

