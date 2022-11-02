import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import os
import numpy as np


def test(path):
    pass


if __name__ == "__main__":
    excel_path = r"E:\code\notes\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    toexcel_path = r"E:\code\notes\noteOnGithub\data\toexcel.xlsx"
    # excel_path = r"D:\lvcode\noteOnGithub\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    # toexcel_path = r"D:\lvcode\noteOnGithub\noteOnGithub\data\toexcel.xlsx"
    sheetName = "黄阁西互通"
    skiprows_sheet = 2
    data_range_in_excel = [[0, 50], [0, 45]]
    dataDf: DataFrame
    dataDf = pd.read_excel(excel_path, sheet_name=sheetName, skiprows=skiprows_sheet, na_filter=0, header=[0, 1, 2, 3])
    # dataDf = pd.read_excel(excel_path, sheet_name=sheetName, skiprows=skiprows_sheet, na_filter=0)
    # print(dataDf.head())
    pd.options.display.max_columns = 10
    # dataDf.dropna(axis=1, how="all", inplace=True)
    # dataDf.dropna(axis=0, how="all", inplace=True)
    # print(dataDf.info)
    dataDf = dataDf.iloc[data_range_in_excel[0][0]:data_range_in_excel[0][1], data_range_in_excel[1][0]:data_range_in_excel[1][1]]
    # print(dataDf.head())

    # 索引清洗
    mi = dataDf.columns
    # print(dataDf.columns)
    mi_df = mi.to_frame(index=False)
    # print(mi_df)
    mi_df_shape = mi_df.shape
    for i in range(0, mi_df_shape[1]):
        mi_df.loc[:, i] = mi_df.loc[:, i].str.replace(r"[ \n\r\t]", "", regex=True) \
            .str.replace(r"Unnamed:.+", "", regex=True)
    # print(mi_df)
    dataDf.columns = pd.MultiIndex.from_frame(mi_df)
    # print(dataDf)
    print(mi_df_shape)

    # 删除空行，空列
    # for i in range(0, mi_df_shape[0]):
    #     print(dataDf.iloc[:, i].map(lambda x: x == ""))
    #     print(f"{i}行:{dataDf.iloc[:, i]}")
    # print(dataDf)
    # print(dataDf.apply(lambda x: np.nan if x == "" else x))
    dataDf.replace("", np.nan, inplace=True)
    dataDf.replace(0, np.nan, inplace=True)
    dataDf.dropna(axis=1, how="all", inplace=True)
    dataDf.dropna(axis=0, how="all", inplace=True)
    # 删除重复行、列
    dataDf.replace(np.nan, "", inplace=True)  # np.nan == np.nan 返回False
    dataDf = dataDf.T.drop_duplicates(keep="first").T

    # print(dataDf[("挖方", "土方", "普通土")])
    # print(dataDf["起讫桩号"])

    # 多层索引列，合并为单层索引
    mulindex = dataDf.columns.to_frame(index=False)
    mulindex_joined = ["-".join(i) for i in mulindex.values]
    dataDf.columns = mulindex_joined

    # res = dataDf.values.str.contains("合计")
    # print(res)

    # print(dataDf.iloc[:, 0], dataDf.iloc[:, 16])
    # dataDf["result"] = np.where(dataDf.iloc[:, 0] == dataDf.iloc[:, 16], "same", "dif")  # np.nan == np.nan 返回False
    # print(dataDf["result"])
    # print(dataDf.iloc[:, 6].map(lambda x:x==""))

    # dataDf.to_excel(toexcel_path)
