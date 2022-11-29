# coding:utf-8
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import os
import numpy as np
import sys


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

    test(1)