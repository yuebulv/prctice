# coding:utf-8
import pandas as pd
# from pandas import DataFrame, Series
# import matplotlib.pyplot as plt
import os
# import numpy as np
# import sys
# from Road.excel_py.road_excel import *


def test(path):
    file_path = r'F:\20211124长寿农村道路\1-CAD\20221128电厂路-起点段不加宽\S-17路基土石方汇总数量表.xls'
    sheet_name = '土石方汇总'
    eval_sentence = '''loc[df["桩号"].str.contains("计", na=False),:]'''
    skiprows = 2
    header = """[0, 1 ,2, 3]"""
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows, header=[0, 1, 2, 3])
    df = df.reset_index()
    df = df.rename(columns=lambda x: x if not 'Unnamed' in str(x) else '')
    df = df.rename(columns={'index': 'ColA'})
    df.columns.names = (None, None, None, None)
    df.columns = [''.join(col) for col in df.columns]
    del df['ColA']
    outpu_path = r'./test.xlsx'
    df.to_excel(outpu_path)


if __name__ == "__main__":
    # sys.path.append(r"./road")
    # # sys.path.append(r"d:/lvcode/prctice/road")
    # print(sys.path)
    # from Road.chain_age import start_end_chainage_split
    # res = start_end_chainage_split("ak0+000")
    # print(res)

    # column_port = demo('qd')
    # print(column_port)

    # excel_name = r'SZYS06010111 每公里土石方数量表汇总表.xls'
    # # excel_name = r'路基、路面排水工程数量表.xls'
    # excel_name = r'公路病害治理工程数量表'
    # column_str = 'qd'
    # road_excel = RoadExcel(excel_name)
    # road_excel_columns = road_excel.get_format_columns()
    # format_column = str_map_factory(column_str, road_excel_columns)
    # print(format_column)

    file_name = r'D:\lvcode\noteOnGithub\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls'
    df = pd.read_excel(file_name, sheet_name='黄阁西互通', skiprows=2)
    df_columns = df.columns
    df_columns_list = list(df_columns)
    df_columns_list = pd.Series(df_columns_list)
    # print(df.head())
    print(df_columns_list)