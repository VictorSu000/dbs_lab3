import MySQLdb
from API import getDB,transNULL


def subbank_add(data):
    r"""
        :param data: a tuple of data consists of all 支行 columns
        :sql param(IN 支行名 varchar(20), IN 所在城市 varchar(20), IN 资产 decimal(15,2))
    """
    db = getDB()
    data = transNULL(data)
    try:
        cur = db.cursor()

        cur.callproc('subbank_add', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception("添加支行失败！")


def subbank_delete(data):
    r"""
        :param data: a tuple of data just consists of subbank name
    """
    db = getDB()
    try:
        cur = db.cursor()

        cur.callproc('subbank_delete', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception("删除支行失败！")


def subbank_update(data):
    r"""
        :param data: a tuple of data (oldname , newname , city , deposit)
    """
    db = getDB()
    data = transNULL(data)
    try:
        cur = db.cursor()

        cur.callproc('subbank_update', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception("更新支行数据失败！")


def subbank_search(conditions):
    r"""
            :param conditions: a tuple of conditions. each element contains "name" and "condition" fields 
    """
    db = getDB()
    try:
        cur = db.cursor()

        sql = "SELECT 名字, 城市, 资产 from 支行 where "
        for con in conditions:
            sql += f"( {con['name']} "
            sslice = con['condition'].split()
            for word in sslice:
                if word=='and' or word=='or':
                    sql += f"{word} {con['name']} "
                else:
                    sql += f"{word} "
            sql += ") and "

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
