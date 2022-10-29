from operator import itemgetter
from itertools import chain
'''
下一步改进方向
1、断链处理存在问题
    处理方法1）改进现在代码
            2）重新写函数，将原路线桩号全部转为不含断链桩号，在成果中将所有桩号转为含断链桩号
2、增加统计路面数量功能
            

'''
import numpy as np
from geopy.distance import geodesic
import math
import roadglobal as roadglobal

def triangleAre(a: float, b: float, c: float):
    # 根据三边长度求面积
    if a + b > c and a + c > b and b + c > a:
        p = (a + b + c) / 2
        area = (p * (p - a) * (p - b) * (p - c))**0.5
        return area
    else:
        return None


if __name__ == "__main__":
    res = roadglobal.regx_eiDat_hdmData()
    print(res)