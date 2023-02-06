#!/usr/bin/python3
# coding: utf-8
import os

import openpyxl

excel = openpyxl.Workbook()
excel.remove(excel[excel.sheetnames[0]])  # 删除第一个默认的表


def mkdir(filepath):
    if not os.path.exists(filepath):
        print("Create dir: " + filepath)
        os.makedirs(filepath)
    else:
        user_input = input("已存在目录，是否删除? (y/n):")
        if user_input == "y":
            print("Create dir: " + filepath)
            os.system("rm -rf " + filepath)
            os.makedirs(filepath)
        else:
            pass