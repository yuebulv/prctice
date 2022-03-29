import re
from operator import itemgetter
import os
from itertools import chain


def getData_list(path, regx, *sortcol, reverse=True, repetition=True):
    '''
    :param path:文件路径
    :param regx:筛选正则表达式
    :param sortcol:排序列，例（2，3, 1） 第2列为主排序列，第3、1列为次排序列
    :param reverse:是否正序排列
    :param repetition:是否去除result中的重复数据
    :return:list，使用regx正则，从path中筛选内容
    '''
    if not os.path.exists(path):
        return f"{path}文件不存在"
    with open(path, 'r') as file:
        fileData = file.read()
    fileData_list = re.findall(regx, fileData, re.MULTILINE)
    # 去重
    if repetition is False:
        fileData_list_singleness = list(set(fileData_list))
        fileData_list_singleness.sort(key=fileData_list.index)
        fileData_list = fileData_list_singleness
    for i in range(0, len(fileData_list)):
        fileData_list[i] = re.findall(r"[^'\"\[\],\s]+", fileData_list[i], re.MULTILINE)
    # 排序
    try:
        sortcol = list(chain.from_iterable(sortcol))
    except TypeError:
        sortcol = list(chain.from_iterable([sortcol]))
    try:
        fileData_list = sorted(fileData_list, key=itemgetter(*sortcol), reverse=reverse)
    except:
        pass
    result = fileData_list
    return result


if __name__ == "__main__":
    path = r"F:\20211124长寿农村道路\纬地\黄水路-20220321新增\踏石路_长寿黄水路slopedata.txt"
    excelRange_output = 'range("ba9")'
    regx = ".+(?:路肩墙|护肩|路堤墙|护脚|类型).+"
    result = getData_list(path, regx, repetition=False)
    print(result)
    # for tem in result:
    #     print(tem)