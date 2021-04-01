import pymysql
import road
import mysql
import re
import slope
import roadglobal
db='长寿支线'
chainage=' a20.'

if __name__ == "__main__":
    # prjpath = r'F:\2020-10-14长寿支线\4-资料\王勇\K -12-16 - 副本\K.prj'
    # prjname = '长寿支线'
    # with mysql.UsingMysql(log_time=False, db=prjname) as um:
    #     sql = f"select 防护类型 from settheprotectiongtypeofslope"
    #     um.cursor.execute(sql)
    #     chainageValuesInTable_list_dic = um.cursor.fetchall()
    #     print(chainageValuesInTable_list_dic)
    # chainageValuesInTable_list = [item[key] for item in chainageValuesInTable_list_dic for key in item]
    # chainages = chainageValuesInTable_list
    # print(chainages)
    b = list(range(1, 10))
    print(b)
    print(type(b))