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
        raise Exception("添加员工失败！")


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
        raise Exception("删除员工数据失败！")


def employee_update(data):
    r"""
        :param data: a tuple of data just consists of 身份证号 and all 员工 columns
        :sql param(IN 身份证号 varchar(18), IN 姓名 varchar(20), IN 联系电话 varchar(20),
        IN 家庭住址 varchar(1024), IN 开始工作日期 DATE, IN 支行名字 varchar(20))
    """
    db = getDB()
    
    try:
        cur = db.cursor()

        # 去除第一个身份证号数据（这里多传一个身份证数据，是为了让各个update接口数据格式一致，均为：主键+所有字段）
        data = data[1:]
        cur.callproc('employee_update', data)

        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception("修改员工数据失败！")



def employee_search(conditions):
    r"""
        :param conditions: a tuple of conditions. each element contains "name" and "condition" fields 
    """
    db = getDB()
    try:
        cur = db.cursor()

        sql = "SELECT 身份证号, 姓名, 联系电话, 家庭住址, 开始工作日期, 支行_名字 from 银行员工 where "
        for con in conditions:
            sql += f"{con['name']} {con['condition']} and "
        
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
        raise Exception("查询员工数据失败！")

if __name__ == '__main__':
    try:
        pass
    except Exception as e:
        print("cannot open mysql due to:\n", e)

