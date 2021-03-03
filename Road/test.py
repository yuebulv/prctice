import pymysql
def check_it():

    with mysql.UsingMysql(log_time=True) as um:
        um.cursor.execute("select count(id) as total from chainage")
        data = um.cursor.fetchone()
        print("-- 当前数量: %d " % data['total'])

if __name__ == "__main__":
    for i in [1,2]:
        print(i)
    # host = 'localhost'
    # port = 3306
    # db = '长寿支线'
    # user = 'root'
    # password = 'sunday'



