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
        raise e


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
        raise e


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
        raise e


def client_search(conditions):
    r"""
        :param conditions: a tuple of conditions. each element contains "name" and "condition" fields 
    """
    db = getDB()
    try:
        cur = db.cursor()

        sql = "SELECT 身份证号, 姓名, 联系电话, 家庭住址, 联系人姓名, 联系人手机号, 联系人Email, 联系人与客户关系 from 银行员工 where "
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
    except Exception as e:
        print("cannot open mysql due to:\n", e)




