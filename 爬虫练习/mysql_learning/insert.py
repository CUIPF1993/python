#!/usr/bin/env python
# encoding: utf-8

"""
@version: python3.6
@author:  CPF 
@contact: cpfyjjs@foxmail.com
@site: 
@software: PyCharm Community Edition
@file: insert.py
@time: 2017/7/31 23:41
"""
import pymysql
db = pymysql.connect('localhost','root','123456','ZHIHU')

cursor = db.cursor()
sql = """INSERT INTO USER(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mas', 'Mohan', 20, 'M', 2000)"""
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    print('插入数据失败')

db.close()