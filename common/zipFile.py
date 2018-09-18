#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''
    文件夹压缩模块：该文件主要对文件夹压缩进行封装
'''

import os,time
import zipfile
import tarfile
import glob

# 尝试小案例 压缩成.zip
class ZipFile(object):
    def __init__(self,sourceFilePath,destFilePath):
        self.source_file = sourceFilePath
        self.dest_file  = destFilePath



    def zip_dir(self):
        sourceFile = self.source_file
        dstFile = self.dest_file
        zipHandle = zipfile.ZipFile(dstFile, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirs, files in os.walk(sourceFile):
            for filename in files:
                print(dirpath, dirs, filename)
                zipHandle.write(os.path.join(dirpath, filename))
                print(filename + " zip succeeded")

        zipHandle.close()
        return dstFile

    def unzip_dir(self,sourceZipFile,dstFile):
        zipHandle = zipfile.ZipFile(sourceZipFile, 'r')
        for filename in zipHandle.namelist():
            print(filename)
        zipHandle.extractall(dstFile)
        zipHandle.close()

    # 压缩tar.gz文件到文件夹
    def tar_dir(self):
        sourceFile = self.source_file
        dstFile = self.dest_file
        tarHandle = tarfile.open(dstFile, 'w:gz')
        for dirpath, dirs, files in os.walk(sourceFile):
            for filename in files:
                tarHandle.add(os.path.join(dirpath, filename))
                print(filename + " tar succeeded ")
        tarHandle.close()

    def untar_dir(self,sourceFile, dstFile):
        tarHandle = tarfile.open(sourceFile, 'r:gz')
        for filename in tarHandle.getnames():
            print(filename)
        tarHandle.extractall(dstFile)
        tarHandle.close()


if __name__ == "__main__":
    # 可以使用相对路径或者绝对路径的文件名或者文件夹的名字
    # 压缩文件
    z = ZipFile("F:\Python_project\PythonLearnning_2018\send_email\sendEmail_Test.html",
                "F:\Python_project\PythonLearnning_2018\send_email\sendEmail_Test.zip")
    z.zip_dir()
    #print("zip ok ")
    #unzip_dir('sendEmail_Test.zip','.\\test_file\\')
    #tar_dir(".\sendEmail_Test.html",".\sendEmail_Test.html.tar.gz")
    #untar_dir(".\sendEmail_Test.html.tar.gz",'.')