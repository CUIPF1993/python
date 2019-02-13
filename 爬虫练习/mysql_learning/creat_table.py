#!/usr/bin/env python
# encoding: utf-8

"""
@version: python3.6
@author:  CPF 
@contact: cpfyjjs@foxmail.com
@site: 
@software: PyCharm Community Edition
@file: creat_table.py
@time: 2017/7/31 23:24
"""

import pymysql

#打开数据库
db = pymysql.connect('localhost','root','123456','ZHIHU')

#使用cursor()方法创建一个游标对象cursor
cursor = db.cursor()

#使用excute() 方法执行SQL，如果表存在删除
cursor.execute("DROP TABLE IF EXISTS USER")

#使用预处理语句创建表
sql = """CREATE TABLE USER (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)
db.close()