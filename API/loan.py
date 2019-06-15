import MySQLdb

from . import getDB

def loan_add(data):
    r"""
    :param data: a tuple of data consists of all 贷款 columns
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('loan_add',data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


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


def fund_add(data):
    r"""
    :param data: a tuple of data consists of all 款项 columns and err code
    """
    db = getDB()

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


def take_loan(data):
    r"""
    :param data: a tuple of data consists of all 借贷 columns
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('take_loan', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


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











