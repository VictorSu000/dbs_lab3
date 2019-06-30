import MySQLdb
from API import getDB,transNULL

def check_leagl(data):
    if data[4]=='支票' and (data[6]!=None or data[7]!=None):
        raise Exception('账户类型与属性不符')
    elif data[4]=='储蓄' and data[8]!=None:
        raise Exception('账户类型与属性不符')

def account_add(data):
    r"""
    :param data: a tuple of data consists of all account columns, 储蓄account columns(except account number)
    and 支票account columns(except account number). Totally 10 values（1 err code)
    Specially, class must be '支票' or '储蓄'
    :sqlparam (IN 账户号 varchar(20), IN 余额 decimal(15,2), IN 开户日期 DATE,IN 支行名 varchar(20), IN 账户类型 varchar(10),
    IN 负责人身份证号 varchar(18), IN 利率 decimal, IN 货币类型 varchar(20), IN 透支余额 decimal, OUT err binary)
    """
    db = getDB()
    data = transNULL(data)
    try:
        cur = db.cursor()
        check_leagl(data)
        # 补充 OUT 字段
        data += ("",)

        cur.callproc('account_add', data)

        cur.execute("select @_account_add_9")
        result = int(cur.fetchall()[0][0])
        if result == 1:
            raise Exception("无效账户类型")

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e

def account_update(data):
    r"""
    :param data: a tuple of data consists of all account columns, 储蓄account columns(except account number)
    and 支票account columns(except account number). Totally 10 values
    Specially, class must be '支票' or '储蓄'
    :sqlparam (IN 身份证号 varchar(18), IN 账户号 varchar(20), IN 余额 decimal(15,2), IN 开户日期 DATE,IN 支行名 varchar(20), IN 账户类型 varchar(10),
    IN 负责人身份证号 varchar(18),IN 利率 decimal, IN 货币类型 varchar(20), IN 透支余额 decimal(15,2))
    PS: class cannot be changed!
    """
    db = getDB()
    data = transNULL(data)

    try:
        cur = db.cursor()
        check_leagl(data)
        # 去除多传的账户号，为了保持接口一致
        data = data[:1] + data[2:]
        cur.callproc('account_update', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


def account_delete(data):
    r"""
    :param data: a tuple of data consists of 账户ID
    :sql param(账户号 varchar(20))
    """
    db = getDB()

    try:
        cur = db.cursor()

        cur.callproc('account_delete', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


def own_account(data):
    r"""
    :param data: a tuple of data consists of 身份证号 and 账户号
    :sql param(身份证号 varchar(18),账户号 varchar(20))
    """
    db = getDB()
    data = transNULL(data)
    try:
        cur = db.cursor()

        cur.callproc('own_account', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise e


def add_conditinos(con,sql):
    sql += f"( {con['name']} "
    sslice = con['condition'].split()
    for word in sslice:
        if word=='and' or word=='or':
            sql += f"{word} {con['name']} "
        else:
            sql += f"{word} "
    sql += ") and "
    return sql

def account_search(conditions):
    r"""
            :param conditions: a tuple of conditions. each element contains "name" and "condition" fields 
    """
    db = getDB()
    try:
        cur = db.cursor()

        sqlc = "SELECT 账户.账户号, 余额, 开户日期, 支行名, 账户类型, 负责人身份证号, 利率, 货币类型, NULL as 透支余额 from 账户,储蓄账户 where 账户.账户号=储蓄账户.账户号 and "
        sqlz = "SELECT 账户.账户号, 余额, 开户日期, 支行名, 账户类型, 负责人身份证号, NULL as 利率, NULL as 货币类型, 透支余额 from 账户,支票账户 where 账户.账户号=支票账户.账户号 and "
        for con in conditions:
            if con['name']== '账户号':
                con['name'] = '账户.账户号'
            if con['name']=='利率' or con['name']=='货币类型':
                sqlc = add_conditinos(con,sqlc)
                sqlz += '账户类型 = \'储蓄\' and ' 
            elif con['name']=='透支余额':
                sqlz = add_conditinos(con,sqlz)
                sqlz += '账户类型 = \'支票\' and ' 
            else:
                sqlc = add_conditinos(con,sqlc)
                sqlz = add_conditinos(con,sqlz)


        sqlc = sqlc[:-4]
        sqlz = sqlz[:-4]

        sql = f"{sqlc} UNION {sqlz}"
        #if sql[-4:] == "and ":
            # 去除多余的 "and "
        #    sql = sql[:-4]
        
        cur.execute(sql)
        return cur.fetchall()
    except Exception as e:
        print(e)
        raise Exception("查询格式错误！")

def own_search(data):
    r"""
            :param conditions: a tuple only contains 账户号 
    """
    db = getDB()
    try:
        cur = db.cursor()

        sql = f"SELECT 账户号,身份证号,最近访问日期 from 拥有账户 where 账户号 = '{data[0]}'"
    
        cur.execute(sql)
        return cur.fetchall()
    except Exception as e:
        print(e)
        raise Exception("查询格式错误！")

if __name__ == '__main__':
    try:
        pass
        # db = MySQLdb.connect(host='localhost', port=3306, user='root', password='123456', db='bank')
        # print('mysql open success')
        # db.autocommit(False)
        # cur = db.cursor()
        # db.set_character_set('utf8')
        # cur.execute('SET NAMES utf8;')
        # cur.execute('SET CHARACTER SET utf8;')
        # cur.execute('SET character_set_connection=utf8;')

        # 实例data，具体请参考函数注释
        # account_add(data=('ZP03', 23454, '2019-02-03', '庞德', '支票', '1003', 0, '0', 5000, 0))
        # 创建账号后加入账号与客户的联系，可以多对多的加，其中会被唯一性表约束
        # cur.callproc('own_account', ('0001', 'ZP04'))
        # db.commit()
        # account_update(data=('0001', 'ZP01', 23454, '2019-02-03', '庞德', '支票', '1002', 0, '0', 5000))
    except Exception as e:
        print("cannot open mysql due to:\n", e)











