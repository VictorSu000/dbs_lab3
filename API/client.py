import MySQLdb
from API import getDB


def client_add(data):
    r"""
        :param data: a tuple of data consists of all 客户 columns
        :sql param(IN 身份证号 varchar(18), IN 姓名 varchar(20), IN 联系电话 varchar(20),
        IN 家庭住址 varchar(1024), IN 联系人姓名 varchar(20), IN 联系人电话varchar(20), IN 联系人邮箱 varchar(100),
        IN 关系 varchar(10))
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
            :sql param(IN 身份证号 varchar(18))
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('client_delete', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def client_update(data):
    r"""
        :param data: a tuple of data consists of all 客户 columns
        :sql param(IN 身份证号 varchar(18), IN 姓名 varchar(20), IN 联系电话 varchar(20),
        IN 家庭住址 varchar(1024), IN 联系人姓名 varchar(20), IN 联系人电话varchar(20), IN 联系人邮箱 varchar(100),
        IN 关系 varchar(10))
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




