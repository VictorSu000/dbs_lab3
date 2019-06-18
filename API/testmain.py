#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import account
import client
import loan
import employee
import subbank
from API import cleanUp

if __name__ == '__main__':
    try:
        # db = MySQLdb.connect(host='localhost', port=3306, user='root', password='417476931', db='bank' ,charset='utf8')
        # print('mysql connect success')
        # db.autocommit(False)
        # cur = db.cursor()
        # cur.execute('SET NAMES utf8;')
        # cur.execute('SET CHARACTER SET utf8;')
        # cur.execute('SET character_set_connection=utf8;')

        #贷款管理模块测试
        #loan.loan_add(data=('DK04', '龙兴', 300000, '未开始发放', 1002))
        #loan.fund_add(data=('KX01', 'DK04', '2019-5-22', 150000, 0))
        #loan.fund_add(data=('KX02', 'DK04', '2019-5-28', 100000, 0))
        #loan.fund_add(data=('KX03', 'DK04', '2019-6-10', 50000, 0))
        #loan.loan_delete(data=('DK04',0))
        #loan.take_loan(data=('DK04', '0001'))
        #loan.take_loan(data=('DK04', '0002'))


        #账户管理模块测试
        #account.account_update(data=('0001', 'CX01', '290000', '2018-03-16', '龙兴', '支票1', '1001', '0.03', 'AUD',0))
        #account.account_add(data=('0002', '290000', '2018-03-16', '龙兴', '支票', '1001', '0.03', 'AUD', 0, 0))
        #account.account_delete(data = ('0001',))
        

        #支行管理
        #subbank.subbank_add(data=('合肥支行','合肥','2'))
        #account.account_add(data=('ZP07', 23454, '2019-02-03', '合肥支行', '支票', '1003', 0, '0', 5000, 0))
        #subbank.subbank_delete(data=('合肥支行',))

        #客户及员工管理
        #client.client_delete(data=('0001',))
        employee.employee_delete(data=('1001',))

    except Exception as e:
        print("cannot open mysql due to:\n", e)