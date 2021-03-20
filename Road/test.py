import pymysql
import road
import mysql
import re
import slope

db='长寿支线'
chainage=' a20.'

if __name__ == "__main__":
    # a=[1,2,3,4]
    # b=['  k - 2020.12.15-更新桥.ctr  ']
    # print(b[0].strip())
    # print(b[0])
    # b[0]=b[0].strip()
    # print(b[0])
    temp = {'id_chainage': 21, 'id': 59, 'chainage': 'A400.000', '左右侧': 1, '3dr中起始位置': 7, '线段个数': 2, '位于边沟左右侧': 2, '边坡类型没用': 0, '坡高': 1.384, '最大级数': 1, '第i级': 1, 'S宽度': 1.038, 'S高度': 1.384, 'S坡度': 0.75, 'P宽度': 0.0, 'P高度': 0.0, 'P坡度': 0.0}
    print(temp.keys())
    print(str(list(temp.values())))
    print(type(temp.values()))


