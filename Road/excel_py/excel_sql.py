"""
目标：实现excel <--> mysql 双向便捷交互

# 1。1 excel_to_excel
  - get_tf_km_age(项目名称，路线，data_source=[excel_name,mysql], axis="返回值轴向") -> [DataFrame,Series]
  - get_tf_km_data(项目名称，路线，起点，止点，data_source=[excel_name,mysql], axis="返回值轴向") -> [DataFrame,Series]
    - return:挖方 【土方（1，2，3类），石方（4,5,6类）】；填方 【土方（1，2，3类），石方（4,5,6类）】
            本桩利用
            远运利用
            借方
            废方
    class sheet_road():
        sheet_tf_km
        sheet_bridgehead_roadbed
        sheet_mud_base
        sheet_protect
        sheet_drain
        sheet_
    class road()
    起点、止点、左幅、右幅、整幅、长度
  - tf.wf.tff.ptt
  - tf.wf.total
## 1.2 mysql_to_excel
# 2.to_mysql


思路：多层索引合并
"""
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import os
import numpy as np


class tf():
    def __init__(self):
        self.wf = "wf"
        self.wf = "t"


def sheet_data_clean(excel_path, columns_label, chain_ages_range):
    # excel_path = r"E:\code\notes\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    # toexcel_path = r"E:\code\notes\noteOnGithub\data\toexcel.xlsx"
    excel_path = r"D:\lvcode\noteOnGithub\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    toexcel_path = r"D:\lvcode\noteOnGithub\noteOnGithub\data\toexcel.xlsx"
    sheetName = "黄阁西互通"
    skiprows_sheet = 2
    data_range_in_excel = [[0, 50], [0, 45]]
    dataDf: DataFrame
    dataDf = pd.read_excel(excel_path, sheet_name=sheetName, skiprows=skiprows_sheet, na_filter=0, header=[0, 1, 2, 3])
    pd.options.display.max_columns = 10
    dataDf = dataDf.iloc[data_range_in_excel[0][0]:data_range_in_excel[0][1],
             data_range_in_excel[1][0]:data_range_in_excel[1][1]]

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
    dataDf.replace("", np.nan, inplace=True)
    dataDf.replace(0, np.nan, inplace=True)
    dataDf.dropna(axis=1, how="all", inplace=True)
    dataDf.dropna(axis=0, how="all", inplace=True)
    # 删除重复行、列
    dataDf.replace(np.nan, "", inplace=True)  # np.nan == np.nan 返回False
    dataDf = dataDf.T.drop_duplicates(keep="first").T

    print(dataDf[("挖方", "土方", "普通土")])
    print(dataDf["起讫桩号"])
    return dataDf["起讫桩号"]


class TfSheet():
    def __init__(self, path, columns_label, chain_ages_range: list = [-1000000, 1000000]):
        self.path = path
        self.chain_ages_range = chain_ages_range
        self.columns_label = columns_label
        columns = {
            "起点": "起点",
            "止点": "起点",
            "起讫桩号": "起讫桩号",
            "长度": "长度",
            "左右幅": "左右幅",
            "挖方总数量": "挖方总数量",
        }
        columns_other_names = {
            "qd": "起点",
            "qqzh": "起讫桩号",
        }

    def get_tf_data(self):
        res = sheet_data_clean(self.path, self.columns_label, self.chain_ages_range)
        print(res)


def main():
    # res = get_tf_data()
    pass


if __name__ == "__main__":
    tf = TfSheet("path", "columns", "chain")
    tf.get_tf_data()




