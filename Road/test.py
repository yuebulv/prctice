import pymysql
import road
import mysql
import re

db='长寿支线'
chainage=' a20.'
temp=road.getChainageFromChainagetable(db,chainage,True)
print(temp)



