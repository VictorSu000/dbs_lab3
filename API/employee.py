import MySQLdb

from API import getDB

def employee_add(data):
    r"""
        :param data: a tuple of data consists of all 员工 columns
        :sql param(IN 身份证号 varchar(18), IN 姓名 varchar(20), IN 联系电话 varchar(20),
        IN 家庭住址 varchar(1024), IN 开始工作日期 DATE, IN 支行名字 varchar(20))
    """
    db = getDB()
    
    try:
        cur = db.cursor()

        cur.callproc('employee_add', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


def employee_delete(data):
    r"""
        :param data: a tuple of data jsut consists of employee ID
        :sql param(IN 身份证号 varchar(18))
    """
    db = getDB()
    
    try:
        cur = db.cursor()

        cur.callproc('employee_delete', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


def employee_update(data):
    r"""
        :param data: a tuple of data just consists of all 员工 columns
        :sql param(IN 身份证号 varchar(18), IN 姓名 varchar(20), IN 联系电话 varchar(20),
        IN 家庭住址 varchar(1024), IN 开始工作日期 DATE, IN 支行名字 varchar(20))
    """
    db = getDB()
    
    try:
        cur = db.cursor()

        cur.callproc('employee_update', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


if __name__ == '__main__':
    try:
        pass
    except Exception as e:
        print("cannot open mysql due to:\n", e)

