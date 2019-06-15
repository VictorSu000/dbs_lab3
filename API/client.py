import MySQLdb
from . import getDB


def client_add(data):
    r"""
        :param data: a tuple of data consists of all 客户 columns
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('client_add',data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def client_delete(data):
    r"""
            :param data: a tuple of data just consists of client ID
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('client_delete', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def client_update(date):
    r"""
            :param data: a tuple of data consists of all 客户 columns
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('client_update', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


if __name__ == '__main__':
    try:
        pass
    except Exception as e:
        print("cannot open mysql due to:\n", e)




