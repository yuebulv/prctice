import pymysql
def check_it():

    with mysql.UsingMysql(log_time=True) as um:
        um.cursor.execute("select count(id) as total from chainage")
        data = um.cursor.fetchone()
        print("-- 当前数量: %d " % data['total'])

if __name__ == "__main__":
    res=[]
    temp='.E:\code\python\prj\prctice.'
    res.append(temp)
    print(temp.find('.'))

    # temp='   '
    res[0]=''
    print(len(res[0]))
    res[0]=res[0].replace('/','\\')
    print(res[0])
    res[0]=res[0].split('\\')
    print(res[0])
    print(res[0][len(res[0])-1])
    print(res)
    print(temp)
    print(temp[len(temp)-1])
    print('\\'.join(temp))



