import MySQLdb


def account_add(db, data):
    r"""
    :param db: database connector
    :param data: a tuple of data consists of all account columns, 储蓄account columns(except account number)
    and 支票account columns(except account number). Totally 10 values（1 err code)
    Specially, class must be '支票' or '储蓄'
    :sqlparam (IN num varchar(20), IN deposite decimal, IN opendate DATE,IN zhname varchar(20), IN class varchar(10),
    IN rate decimal, IN curclass varchar(20), IN zpdeposite decimal, OUT err binary)
    """
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

def account_update(db, data):
    r"""
    :param db: database connector
    :param data: a tuple of data consists of all account columns, 储蓄account columns(except account number)
    and 支票account columns(except account number). Totally 9 values(without err code)
    Specially, class must be '支票' or '储蓄'
    :sqlparam (IN id varchar(18), IN num varchar(20), IN deposite decimal, IN opendate DATE,IN zhname varchar(20), IN class varchar(10),
    IN rate decimal, IN curclass varchar(20), IN zpdeposite decimal)
    PS: class cannot be changed!
    """
    try:
        cur = db.cursor()

        cur.callproc('account_update', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def account_delete(db, data):
    r"""
    :param db: database connector
    :param data: a tuple of data consists of all
    """
    try:
        cur = db.cursor()

        cur.callproc('account_delete', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def own_account(db, data):
    r"""
    :param db: database connector
    :param data: a tuple of data consists of 身份证号 and 账户号
    """
    try:
        cur = db.cursor()

        cur.callproc('own_account', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


if __name__ == '__main__':
    try:
        db = MySQLdb.connect(host='localhost', port=3306, user='root', password='123456', db='bank')
        print('mysql open success')
        db.autocommit(False)
        cur = db.cursor()
        db.set_character_set('utf8')
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')

        # 实例data，具体请参考函数注释
        # account_add(db, data=('ZP03', 23454, '2019-02-03', '庞德', '支票', '1003', 0, '0', 5000, 0))
        # 创建账号后加入账号与客户的联系，可以多对多的加，其中会被唯一性表约束
        # cur.callproc('own_account', ('0001', 'ZP04'))
        # db.commit()
        # account_update(db, data=('0001', 'ZP01', 23454, '2019-02-03', '庞德', '支票', '1002', 0, '0', 5000))

        db.close()
    except Exception as e:
        print("cannot open mysql due to:\n", e)










