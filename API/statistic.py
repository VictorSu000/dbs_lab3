import MySQLdb
from API import getDB

def statistic_search(conditions):
    r"""
        :param conditions: a tuple of conditions. each element contains "name" and "condition" fields 
        :conditions: business class and time interval
    """
    db = getDB()

    print(conditions)

    try:
        cur = db.cursor()
        date_cmp = f"date_add(日期,interval str_to_date(\'{conditions[1]['condition']}\','%Y-%m-%d') YEAR_MONTH) > date_format(now(),'%Y-%m-%d')"
        print(date_cmp)

        if(conditions[0]['condition']=='储蓄'):
            sql = f"SELECT 支行,业务总金额,用户数 from (SELECT 支行,SUM(金额) as 业务总金额 from 储蓄业务 where {date_cmp}) t1," + \
                f"(SELECT 支行名,COUNT(distinct 身份证号) as 用户数 from 账户,拥有账户 where 账户.账户号 = 拥有账户.账户号 and date_add(最近访问日期,interval \'{conditions[1]['condition']}'\' YEAR_MONTH) > date_format(now(),'%Y-%m-%d')) t2 "+ \
                "where t1.支行 = t2.支行名"
        else:
            sql = f"SELECT t1.名字 as 支行,业务总金额,用户数 from (SELECT 名字,SUM(金额) as 业务总金额 from 贷款 where 贷款号 in (SELECT 贷款号 from 款项 where {date_cmp})) t1,"+ \
                f"(SELECT 名字,COUNT(distinct 身份证号) as 用户数 from 贷款,借贷 where 贷款.贷款号 = 借贷.贷款号 and 贷款.贷款号 in (SELECT 贷款号 from 款项 where {date_cmp})) t2 "+ \
                "where t1.名字 = t2.名字"

        cur.execute(sql)
        return cur.fetchall()

    except Exception as e:
        print(e)
        raise Exception("查询格式错误！")