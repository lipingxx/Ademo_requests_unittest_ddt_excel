#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 读取config.ini配置文件

import os
import configparser

# config
cur_path = os.path.dirname(os.path.relpath(__file__))
configPath = os.path.join(cur_path,'config.ini')
conf = configparser.ConfigParser()
conf.read(configPath)

def get_smtpServer(smtpServer):
    smtp_server = conf.get('email',smtpServer)
    return smtp_server

def get_sender(sender):
    sender = conf.get('email',sender)
    return sender

def get_pwd(pwd):
    pwd = conf.get('email',pwd)
    return pwd

def get_port(port):
    port = conf.get('email',port)
    return port

def get_receiver(receiver):
    receiver = conf.get('email',receiver)
    return receiver

def get_subject(subject):
    subject = conf.get('email',subject)
    return subject

def get_excelPath(excelPath):
    excelPath = conf.get('interfaceData',excelPath)
    return excelPath

def get_excelName(excelName):
    excelName = conf.get('interfaceData',excelName)
    return excelName

