import re
from operator import itemgetter
import os
from itertools import chain


def getData_list(path, regx, *sortcol, reverse=True, repetition=True, en="UTF-8"):
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
    with open(path, 'r', encoding=en) as file:
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


def getFileData_list(path, regx, *sortcol, reverse=True, repetition=True, en="UTF-8"):
    pass
