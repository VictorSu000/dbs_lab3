import MySQLdb

from . import getDB

def employee_add(data):
    r"""
            :param data: a tuple of data consists of all 员工 columns
    """
    db = getDB()
    
    try:
        cur = db.cursor()

        cur.callproc('employee_add', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def employee_delete(data):
    r"""
            :param data: a tuple of data jsut consists of employee ID
    """
    db = getDB()
    
    try:
        cur = db.cursor()

        cur.callproc('employee_delete', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def employee_update(data):
    r"""
            :param data: a tuple of data just consists of all 员工 columns
    """
    db = getDB()
    
    try:
        cur = db.cursor()

        cur.callproc('employee_update', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


if __name__ == '__main__':
    try:
        pass
    except Exception as e:
        print("cannot open mysql due to:\n", e)

