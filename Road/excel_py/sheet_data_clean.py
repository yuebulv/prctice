# coding:utf-8
'''
功能：对dataframe中数据清洗
'''
import pandas as pd
from pandas import DataFrame, Series
import numpy as np


def clean_sheet_data(data_df: DataFrame) -> DataFrame:
    dataDf: DataFrame = data_df.copy()
    pd.options.display.max_columns = 10

    # 索引清洗
    mi = dataDf.columns
    mi_df = mi.to_frame(index=False)
    mi_df_shape = mi_df.shape
    for i in range(0, mi_df_shape[1]):
        mi_df.loc[:, i] = mi_df.loc[:, i].str.replace(r"[ \n\r\t]", "", regex=True) \
            .str.replace(r"Unnamed:.+", "", regex=True)
    dataDf.columns = pd.MultiIndex.from_frame(mi_df)
    with pd.ExcelWriter(r'.\sheet_data_clean.xlsx', mode="a") as writer:
        dataDf.to_excel(writer, sheet_name="sheet2")

    # 忽略隐藏列*************需补充****************

    # 删除空行，空列
    dataDf.replace("", np.nan, inplace=True)
    dataDf.replace(0, np.nan, inplace=True)
    # dataDf.dropna(axis=1, how="all", inplace=True)
    dataDf.dropna(axis=0, how="all", inplace=True)
    with pd.ExcelWriter(r'.\sheet_data_clean.xlsx', mode="a") as writer:
        dataDf.to_excel(writer, sheet_name="sheet3")

    # # 删除重复行、列
    # dataDf.replace(np.nan, "", inplace=True)  # np.nan == np.nan 返回False
    # dataDf = dataDf.T.drop_duplicates(keep="first").T

    # 多层索引合并为单层索引
    # 方法一 可行
    # mi_df = dataDf.columns.to_frame(index=False)
    # print("mi_df:", mi_df)
    # # mi_df.fillna(method='ffill', inplace=True)
    # # print("mi_df:", mi_df)
    # # quit()
    # for row_index in range(0, mi_df.shape[-1]):
    #     print(mi_df.iloc[:, row_index])
    #     try:
    #         mi_df["cat"] = mi_df['cat'] + mi_df.iloc[:, row_index]
    #     except KeyError:
    #         mi_df["cat"] = mi_df.iloc[:, row_index]
    #     print("mi_df[cat]", mi_df["cat"])
    # dataDf.columns = mi_df["cat"]

    # 方法二
    dataDf.columns = [''.join(list(col_tuple)) for col_tuple in dataDf.columns]
    # with pd.ExcelWriter(r'.\sheet_data_clean.xlsx', mode="a") as writer:
    #     dataDf.to_excel(writer, sheet_name="sheet4")
    # quit()



    # 删除重复列索引，索引相同时判断值是否相等，如果不等则拼接到一起
    dataDf_dup: DataFrame = dataDf.iloc[:, dataDf.columns.duplicated(keep=False)]
    dataDf = dataDf.iloc[:, ~dataDf.columns.duplicated(keep="first")]
    columnss_dup = dataDf_dup.columns.unique()
    for column_dup in columnss_dup:
        dataDf_column_dup: DataFrame = dataDf_dup[column_dup]
        dataDf_column_dup = dataDf_column_dup.copy()  # 消除警告pandas A value is trying to be set on a copy of a slice from a DataFrame
        for index_dataDf_column_dup in range(0, dataDf_column_dup.shape[0]):
            tem = list(dataDf_column_dup.iloc[index_dataDf_column_dup, :].unique())
            tem = [str(i) for i in tem]
            tem = "".join(tem).replace("nan", "")
            try:
                dataDf_column_dup.iloc[index_dataDf_column_dup, 0] = tem
            except IndexError:
                dataDf_column_dup.iloc[index_dataDf_column_dup, 0] = ""
        # print("dataDf_column_dup", dataDf_column_dup)
        dataDf_column_dup = dataDf_column_dup.iloc[:, ~dataDf_column_dup.columns.duplicated(keep="first")]
        dataDf[column_dup] = dataDf_column_dup[column_dup]
    dataDf.to_excel(r'.\sheet_data_clean.xlsx')
    return dataDf


def demo():
    # sys.path.append(r"./road")
    # from Road.chain_age import start_end_chainage_split
    # # toexcel_path = r"E:\code\notes\noteOnGithub\data\toexcel.xlsx"
    # toexcel_path = r"D:\lvcode\noteOnGithub\noteOnGithub\data\toexcel.xlsx"
    # sheetName = sheet_name
    # skiprows_sheet = skiprows
    # dataDf: DataFrame
    # dataDf = pd.read_excel(excel_path, sheet_name=sheetName, skiprows=skiprows_sheet, na_filter=0, header=header)
    # pd.options.display.max_columns = 10

    # 设置sheet_name中数据范围
    # data_range_in_excel = [[0, 50], [0, 45]]
    # dataDf = dataDf.iloc[data_range_in_excel[0][0]:data_range_in_excel[0][1],
    #          data_range_in_excel[1][0]:data_range_in_excel[1][1]]

    pass
