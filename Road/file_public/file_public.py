import re
from operator import itemgetter
import os
from itertools import chain
import pandas as pd
from pandas import DataFrame, Series
import sys


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


def file_filter_list(file_filter: list, path_str) -> list:
    # 功能：得到filter类型文件路径,[文件名, 文件路径]
    file_list = []
    for root, dirs, files in os.walk(path_str, topdown=False):
        for name in files:
            tem = os.path.join(root, name)
            if tem.split('.')[-1] in file_filter:
                file_list.append([name, tem])
    return file_list


def get_contents_excel(path_str) -> DataFrame:
    # 功能：得到path_str路径下所有的excel[文件名, 文件路径，工作表1，工作表n]
    # return: DataFrame, 列索引[file_name, file_path，sheet_name1，sheet_namen]
    # sys.path.append(r'./road')
    # from Road.file_public.file_public import file_filter_list
    file_path_list = file_filter_list(['xlsx', 'xls'], path_str=path_str)
    files_sheet_names_list = []
    max_sheet_count = 0
    for file_path in file_path_list:
        xl = pd.ExcelFile(file_path[-1])
        file_sheet_names = xl.sheet_names
        files_sheet_names_list.append(file_sheet_names)
        max_sheet_count = max(max_sheet_count, len(file_sheet_names))
    column_labels = ['sheet_name' + str(i) for i in range(0, max_sheet_count)]
    files_sheet_names_df = pd.DataFrame(files_sheet_names_list, columns=column_labels)
    data_df = pd.DataFrame(file_path_list, columns=['file_name', 'file_path'])
    data_df = pd.concat([data_df, files_sheet_names_df], axis=1)
    return data_df


if __name__ == "__main__":
    path_str = r'D:\lvcode\noteOnGithub\noteOnGithub\data'
    res = file_filter_list(['xlsx', 'xls'], path_str=path_str)
    print(res)