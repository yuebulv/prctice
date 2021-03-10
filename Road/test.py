# import pymysql
# def check_it():
#
#     with mysql.UsingMysql(log_time=True,db='长寿支线2') as um:
#         um.cursor.execute("select count(id) as total from chainage")
#         data = um.cursor.fetchone()
#         print("-- 当前数量: %d " % data['total'])
#
# if __name__ == "__main__":
#     check_it()
import pymysql
databaseName='cszx'
prjname = databaseName
conn = pymysql.connect(user="root", passwd="sunday")  # ,db = "mysql")
cursor = conn.cursor()
cursor.execute(f'CREATE DATABASE IF NOT EXISTS {prjname} DEFAULT CHARSET utf8 COLLATE utf8_general_ci;')
conn.select_db(prjname)
cursor.execute('drop table if exists chainage')
sql = """CREATE TABLE IF NOT EXISTS `chainage` (
      `id` int(6) NOT NULL AUTO_INCREMENT,
      `id_last` int(6) ,
      `chainage` varchar(50) NOT NULL,
      `chainage_noBreakChain` int(50) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
cursor.execute(sql)
cursor.close()
conn.commit()
conn.close()


