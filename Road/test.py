import pymysql
import road
import mysql
import re
import slope

db='长寿支线'
chainage=' a20.'

if __name__ == "__main__":
    res_dic = {'起点': '', '止点': '', '长度': ''}
    temp = 1