import MySQLdb


def employee_add(db,data):
    r"""
            :param db: database connector
            :param data: a tuple of data consists of all 员工 columns
    """
    try:
        cur = db.cursor()

        cur.callproc('employee_add', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def employee_delete(db,data):
    r"""
            :param db: database connector
            :param data: a tuple of data jsut consists of employee ID
    """
    try:
        cur = db.cursor()

        cur.callproc('employee_delete', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def employee_update(db,data):
    r"""
            :param db: database connector
            :param data: a tuple of data just consists of all 员工 columns
    """
    try:
        cur = db.cursor()

        cur.callproc('employee_update', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


if __name__ == '__main__':
    try:
        db = MySQLdb.connect(host='localhost', port=3306, user='root', password='417476931', db='bank')
        print('mysql open success')
        db.autocommit(False)
        cur = db.cursor()
        db.set_character_set('utf8')
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')

        db.close()
    except Exception as e:
        print("cannot open mysql due to:\n", e)
