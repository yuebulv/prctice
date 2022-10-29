import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import os
import numpy as np


def test(path):
    pass


if __name__ == "__main__":
    excel_path = r"E:\code\notes\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    sheetName = "黄阁西互通"
    skiprows_sheet = 2
    toexcel_path = r"E:\code\notes\noteOnGithub\data\toexcel.xlsx"
    dataDf: DataFrame
    dataDf = pd.read_excel(excel_path, sheet_name=sheetName, skiprows=skiprows_sheet, na_filter=0, header=[0, 1, 2, 3])
    print(dataDf.head())
    pd.options.display.max_columns = 10
    print(dataDf.shape)
    dataDf.dropna(axis=1, how="all", inplace=True)
    print(dataDf.shape)
    dataDf.dropna(axis=0, how="all", inplace=True)
    print(dataDf.shape)
    # dataDf.drop(columns=["Unnamed: 51"], inplace=True)
    dataDf.to_excel(toexcel_path)
    newDf = dataDf.loc[0:4]
    print(newDf)