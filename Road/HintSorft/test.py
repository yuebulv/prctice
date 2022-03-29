from operator import itemgetter
from itertools import chain
'''
下一步改进方向
1、断链处理存在问题
    处理方法1）改进现在代码
            2）重新写函数，将原路线桩号全部转为不含断链桩号，在成果中将所有桩号转为含断链桩号
2、增加统计路面数量功能
            

'''


def loadDataToExcel_regx(path, *sortcol, repetition=True):
    print("path:",path)
    print('rep:',repetition)
    print('sort:',sortcol)
    print(*sortcol)


if __name__ == "__main__":
    list_tem = [["a",2,5], ["k",5,2],["w",2,3],["w",1,3],["a",1,3]]
    ss = sorted(list_tem, key=itemgetter(2,1,0))
    print(ss)
    # my_list = [2, 1, 0]
    my_list = (2, 1, 0)
    ss1 = sorted(list_tem, key=itemgetter(*my_list), reverse=True)
    print(ss1)
    # tem = [2,1,0]
    # tem1 = (tem,[2])
    # tem2 =list(chain.from_iterable(tem1))
    print(list([7]))