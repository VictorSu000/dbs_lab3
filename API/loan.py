import MySQLdb

from API import getDB,transNULL

def loan_add(data):
    r"""
    :param data: a tuple of data consists of all 贷款 columns
    :sql param(IN 贷款号 varchar(20), IN 名字 varchar(20), IN 金额 decimal(15,2),
    IN 状态 varchar(45), IN 负责人身份证号 varchar(18))
    """
    db = getDB()
    data = transNULL(data)
    try:
        cur = db.cursor()

        cur.callproc('loan_add',data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


def loan_delete(data):
    r"""
    :param data: a tuple of data consists of 贷款号 and err code ( for refusal of deleting "发放中" state loans)
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('loan_delete', data)

        cur.execute("select @_loan_delete_1")
        result = int(cur.fetchall()[0][0])
        if result == 1:
            raise Exception("无法删除发放中的贷款")

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


def fund_add(data):
    r"""
    :param data: a tuple of data consists of all 款项 columns and err code
    :sql param(IN 款项号 varchar(10), IN 贷款号 varchar(20), IN 日期 DATE,
    IN 金额 decimal(15,2), OUT err binary)
    """
    db = getDB()
    data = transNULL(data)
    try:
        cur = db.cursor()

        cur.callproc('fund_add', data)

        cur.execute('select @_fund_add_4')
        result = int(cur.fetchall()[0][0])
        if result == 1:
            raise Exception('此笔款项超过可发放的贷款总金额')

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


def take_loan(data):
    r"""
    :param data: a tuple of data consists of all 借贷 columns
    :sql param(IN 贷款号 varchar(20), IN 身份证号 varchar(18))
    """
    db = getDB()
    data = transNULL(data)
    try:
        cur = db.cursor()

        cur.callproc('take_loan', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e

def loan_search(conditions):
    r"""
        :param conditions: a tuple of conditions. each element contains "name" and "condition" fields 
    """
    db = getDB()
    try:
        cur = db.cursor()

        sql = "SELECT 贷款号, 名字, 金额, 状态, 负责人身份证号 from 贷款 where "
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

if __name__ == '__main__':
    try:
        pass

        # 实例data，具体请参考函数注释
        # cur.callproc('loan_add', ('DK02', '龙兴', 50000, '未开始发放'))
        # db.commit()
        # loan_delete(('DK01', 0))
        # cur.callproc('fund_add', ('KX03', 'DK01', '2018-12-25', 10000))
        # db.commit()

    except Exception as e:
        print("cannot open mysql due to:\n", e)











