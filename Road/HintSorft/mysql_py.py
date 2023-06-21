# coding=utf-8
import pymysql


def insertDataToMysql(databaseName, sql, data):
    conn = pymysql.connect(user="root", passwd="sunday")
    cursor = conn.cursor()
    conn.select_db(databaseName)
    massage_str = 'insertDataToMysql：插入数据失败'
    try:
        insert = cursor.execute(sql, data)
    except:
        for data_of_table in data:
            # sql = "insert into pavement values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            insert = cursor.execute(sql, data_of_table)
    massage_str = 'insertDataToMysql：插入数据成功'
    cursor.close()
    conn.commit()
    conn.close()

    return massage_str


if __name__ == "__main__":
    tem = [1]
    le = len(tem)
    print(le)
    print(isinstance(tem, list))