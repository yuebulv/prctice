import pymysql
if __name__ == "__main__":
    prjname = '长寿支线'
    # temp=road.setupC
    conn = pymysql.connect(user="root", passwd="sunday")  # ,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)

    sql = r'load data infile "F:\2020-10-14长寿支线\4-资料\王勇\K -12-16 - 副本\load.txt" into table  drainageditch fields terminated by "\t"'
    insert = cursor.execute(sql)

    cursor.close()
    conn.commit()
    conn.close()


    print()