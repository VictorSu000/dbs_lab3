import MySQLdb
from API import getDB

def account_add(data):
    r"""
    :param data: a tuple of data consists of all account columns, 储蓄account columns(except account number)
    and 支票account columns(except account number). Totally 10 values（1 err code)
    Specially, class must be '支票' or '储蓄'
    :sqlparam (IN 账户号 varchar(20), IN 余额 decimal(15,2), IN 开户日期 DATE,IN 支行名 varchar(20), IN 账户类型 varchar(10),
    IN 利率 decimal, IN 货币类型 varchar(20), IN 透支余额 decimal, OUT err binary)
    """
    db = getDB()
    try:
        cur = db.cursor()

        cur.callproc('account_add', data)

        cur.execute("select @_account_add_9")
        result = int(cur.fetchall()[0][0])
        if result == 1:
            raise Exception("无效账户类型")

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e

def account_update(data):
    r"""
    :param data: a tuple of data consists of all account columns, 储蓄account columns(except account number)
    and 支票account columns(except account number). Totally 9 values(without err code)
    Specially, class must be '支票' or '储蓄'
    :sqlparam (IN 身份证号 varchar(18), IN 账户号 varchar(20), IN 余额 decimal(15,2), IN 开户日期 DATE,IN 支行名 varchar(20), IN 账户类型 varchar(10),
    IN 利率 decimal, IN 货币类型 varchar(20), IN 透支余额 decimal(15,2))
    PS: class cannot be changed!
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('account_update', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


def account_delete(data):
    r"""
    :param data: a tuple of data consists of 账户ID
    :sql param(账户号 varchar(20))
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('account_delete', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


def own_account(data):
    r"""
    :param data: a tuple of data consists of 身份证号 and 账户号
    :sql param(身份证号 varchar(18),账户号 varchar(20))
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('own_account', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e

def account_search(conditions):
    r"""
            :param conditions: a tuple of conditions. each element contains "name" and "condition" fields 
    """
    db = getDB()
    try:
        cur = db.cursor()

        sql = "SELECT 账户号, 余额, 开户日期, 支行名, 账户类型, 负责人身份证号 from 支行 where "
        for con in conditions:
            sql += f"{con['name']} "
            sslice = con['condition'].split()
            for word in sslice:
                if word=='and' or word=='or':
                    sql += f"{word} {con['name']} "
                else:
                    sql += f"{word} "
            sql += "and "

        if sql[-4:] != "and ":
            # 没有任何条件，去除最后的 "where "
            sql = sql[:-6]
        else:
            # 去除多余的 "and "
            sql = sql[:-4]
        
        cur.execute(sql)
        return cur.fetchall()
    except Exception as e:
        print(e)
        raise Exception("查询格式错误！")

if __name__ == '__main__':
    try:
        pass
        # db = MySQLdb.connect(host='localhost', port=3306, user='root', password='123456', db='bank')
        # print('mysql open success')
        # db.autocommit(False)
        # cur = db.cursor()
        # db.set_character_set('utf8')
        # cur.execute('SET NAMES utf8;')
        # cur.execute('SET CHARACTER SET utf8;')
        # cur.execute('SET character_set_connection=utf8;')

        # 实例data，具体请参考函数注释
        # account_add(data=('ZP03', 23454, '2019-02-03', '庞德', '支票', '1003', 0, '0', 5000, 0))
        # 创建账号后加入账号与客户的联系，可以多对多的加，其中会被唯一性表约束
        # cur.callproc('own_account', ('0001', 'ZP04'))
        # db.commit()
        # account_update(data=('0001', 'ZP01', 23454, '2019-02-03', '庞德', '支票', '1002', 0, '0', 5000))
    except Exception as e:
        print("cannot open mysql due to:\n", e)











