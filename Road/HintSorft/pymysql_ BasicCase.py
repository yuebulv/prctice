if __name__=="__main__":
    import pymysql
    #打开数据库连接
    conn = pymysql.connect(user = "root",passwd = "sunday")#,db = "mysql")
    # conn.select_db('mysql')
    # 获取游标
    cursor = conn.cursor()
    # 创建pythonBD数据库
    cursor.execute('CREATE DATABASE IF NOT EXISTS pythonDB DEFAULT CHARSET utf8 COLLATE utf8_general_ci;')
    conn.select_db('pythonDB')
    # 创建user表
    cursor.execute('drop table if exists user')
    sql = """CREATE TABLE IF NOT EXISTS `user` (
    	  `id` int(11) NOT NULL AUTO_INCREMENT,
    	  `name` varchar(255) NOT NULL,
    	  `age` int(11) NOT NULL,
    	  PRIMARY KEY (`id`)
    	) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
    cursor.execute(sql)
    insert = cursor.execute("insert into user values(1,'tom',18)")
    print('添加语句受影响的行数：', insert)

    # 另一种插入数据的方式，通过字符串传入值
    sql = "insert into user values(%s,%s,%s)"
    cursor.execute(sql, (3, 'kongsh', 20))


    # 另一种插入数据的方式，通过字符串传入值
    sql = "insert into user values(%s,%s,%s)"
    insert = cursor.executemany(sql, [(4, 'wen', 20), (5, 'tom', 10), (6, 'test', 30)])
    print('批量插入返回受影响的行数：', insert)

    cursor.execute("select * from user;")
    while 1:
        res = cursor.fetchone()
        if res is None:
            # 表示已经取完结果集
            break
        print(res)

    cursor.execute('select * from user')
    # 取3条数据
    resTuple = cursor.fetchmany(3)
    print(type(resTuple))
    for res in resTuple:
        print(res)

    cursor.execute('select * from user')
    # 取所有数据
    resTuple = cursor.fetchall()
    print(type(resTuple))
    print('共%d条数据' % len(resTuple))

    update = cursor.execute("update user set age=100 where name='kongsh'")
    print('修改后受影响的行数为：', update)
    # 查询一条数据
    cursor.execute('select * from user where name = "kongsh";')
    print(cursor.fetchone())

    # 更新前查询所有数据
    cursor.execute("select * from user where name in ('kongsh','wen');")
    print('更新前的数据为：')
    for res in cursor.fetchall():
        print(res)

    print('*' * 40)
    # 更新2条数据
    sql = "update user set age=%s where name=%s"
    update = cursor.executemany(sql, [(15, 'kongsh'), (18, 'wen')])

    # 更新2条数据后查询所有数据
    cursor.execute("select * from user where name in ('kongsh','wen');")
    print('更新后的数据为：')
    for res in cursor.fetchall():
        print(res)

    # 删除前查询所有数据
    cursor.execute("select * from user;")
    print('删除前的数据为：')
    for res in cursor.fetchall():
        print(res)

    print('*' * 40)
    # 删除1条数据
    cursor.execute("delete from user where id=1")

    # 删除后查询所有数据
    cursor.execute("select * from user;")
    print('删除后的数据为：')
    for res in cursor.fetchall():
        print(res)

    cursor.close()
    conn.commit()
    conn.close()

