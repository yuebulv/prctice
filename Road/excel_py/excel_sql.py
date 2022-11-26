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

# 表格符合性检查

思路：多层索引合并
"""
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import os
import numpy as np
import re
import sys


class tf():
    def __init__(self):
        self.wf = "wf"
        self.wf = "t"
    def wf(self):
        pass
        def tff(self):
            pass
            def ptt(self):
                pass


class TfSheet():
    def __init__(self, path, sheet_name, columns_label, chain_ages_range: list = [-1000000, 1000000]):
        self.path = path
        self.sheet_name = sheet_name
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
            "起点": ["qd"],
            "挖方总数量": ["挖方", "wf"],
        }

    # def dataframe_init(self):
    #     dataframe = sheet_data_clean(self.path, self.sheet_name)
    #     self.dataframe = dataframe
    #
    # def get_tf_data(self):
    #     res = sheet_data_clean(self.path, self.columns_label, self.chain_ages_range)
    #     print(res)
    #
    # def loc(self):
    #     return self.dataframe.loc


class TfSheetCheck():
    pass


class TfSheetCheckRule():
    pass


# def start_end_chainage_split(start_end_chainage: str) -> list:
#     # 例GAK36+086.363-GAK37+000，返回[36086.363, 37000, GA]
#     start_end_chainage = start_end_chainage.upper()
#     regx = r"[-]*[\d+.]+"
#     chain_list = re.findall(regx, start_end_chainage, re.MULTILINE)
#     for i in range(0, len(chain_list)):
#         chain_list[i] = chain_list[i].replace("+", "")
#     regx = r"[A-J|L-Z]+"
#     try:
#         road_name = re.findall(regx, start_end_chainage, re.MULTILINE)[0]
#     except IndexError:
#         road_name = ""
#     chain_list.append(road_name)
#     return chain_list


def sheet_data_clean(excel_path, sheet_name, skiprows=None, header=0):
    sys.path.append(r"./road")
    from Road.chain_age import start_end_chainage_split
    # toexcel_path = r"E:\code\notes\noteOnGithub\data\toexcel.xlsx"
    toexcel_path = r"D:\lvcode\noteOnGithub\noteOnGithub\data\toexcel.xlsx"
    sheetName = sheet_name
    skiprows_sheet = skiprows
    dataDf: DataFrame
    dataDf = pd.read_excel(excel_path, sheet_name=sheetName, skiprows=skiprows_sheet, na_filter=0, header=header)
    pd.options.display.max_columns = 10

    # 设置sheet_name中数据范围
    # data_range_in_excel = [[0, 50], [0, 45]]
    # dataDf = dataDf.iloc[data_range_in_excel[0][0]:data_range_in_excel[0][1],
    #          data_range_in_excel[1][0]:data_range_in_excel[1][1]]

    # 索引清洗
    mi = dataDf.columns
    mi_df = mi.to_frame(index=False)
    mi_df_shape = mi_df.shape
    for i in range(0, mi_df_shape[1]):
        mi_df.loc[:, i] = mi_df.loc[:, i].str.replace(r"[ \n\r\t]", "", regex=True) \
            .str.replace(r"Unnamed:.+", "", regex=True)
    dataDf.columns = pd.MultiIndex.from_frame(mi_df)

    # 忽略隐藏列*************需补充****************

    # 删除空行，空列
    dataDf.replace("", np.nan, inplace=True)
    dataDf.replace(0, np.nan, inplace=True)
    dataDf.dropna(axis=1, how="all", inplace=True)
    dataDf.dropna(axis=0, how="all", inplace=True)
    # with pd.ExcelWriter(toexcel_path, mode="a") as writer:
    #     dataDf.to_excel(writer, sheet_name="sheet3")

    # # 删除重复行、列
    # dataDf.replace(np.nan, "", inplace=True)  # np.nan == np.nan 返回False
    # dataDf = dataDf.T.drop_duplicates(keep="first").T

    # 多层索引合并为单层索引
    mi_df = dataDf.columns.to_frame(index=False)
    # print("mi_df:", mi_df)
    for row_index in range(0, mi_df.shape[-1]):
        # print(mi_df.iloc[:, row_index])
        try:
            mi_df["cat"] = mi_df['cat'] + mi_df.iloc[:, row_index]
        except KeyError:
            mi_df["cat"] = mi_df.iloc[:, row_index]
        # print("mi_df[cat]", mi_df["cat"])
    dataDf.columns = mi_df["cat"]
    # print("dataDf.columns:", dataDf.columns)
    # print("mi_df:", mi_df)

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

    # 增加起点、止点列、路线前缀
    # start_end_chainage_split_df: DataFrame = dataDf["起讫桩号"].map(start_end_chainage_split) \
    #     .map(lambda x: ",".join(x)).str.split(",", expand=True)
    # start_end_chainage_split_df.replace("", np.nan, inplace=True)
    # start_end_chainage_split_df.rename(columns={0: "起点", 1: "止点", 2: "路线前缀"}, inplace=True)
    # dataDf[start_end_chainage_split_df.columns] = start_end_chainage_split_df
    # dataDf['起点'] = dataDf['起点'].astype(float)
    # dataDf['止点'] = dataDf['止点'].astype(float)

    # start_end_chainage_split_df.to_excel(toexcel_path)
    # with pd.ExcelWriter(toexcel_path, mode="a") as writer:
    #     dataDf.to_excel(writer, sheet_name="sheet1")
    dataDf.to_excel(toexcel_path)
    return dataDf


def tf_km_sheet_data(eval_sentence):

    return eval(eval_sentence)


def get_sheet_data(file_name, sheet_name, eval_sentence, skiprows=None, header="0", sheet_type="road"):
    '''
    :param file_name:要查询文件的路径+文件名
    :param sheet_name:要查询表格name
    :param eval_sentence:执行的查询语句,如"""loc[df["起讫桩号"]=="合计", '挖方总数量']"""，不需要在前面加df.
    :param skiprows:需要忽略前N行，int
    :param header:表头所在行，例"""[0, 1 ,2]"""，从skiprow之后开始计
    :param sheet_type:如果为road,则运行函数start_end_chainage_split_df（根据起讫桩号添加列：起点、止点、路线编号）
    :return:
    '''
    skiprows = eval(skiprows)
    header = eval(header)
    df: DataFrame = sheet_data_clean(file_name, sheet_name, skiprows, header)
    if sheet_type.lower() == 'road':
        sys.path.append(r"./road")
        from Road.chain_age import start_end_chainage_split_df
        df = start_end_chainage_split_df(df)
    return eval("df" + "." + eval_sentence)


def main():
    # res = get_tf_data()
    pass


if __name__ == "__main__":
    # tf = TfSheet("path", "columns", "chain")
    # tf.get_tf_data()

    # excel_path = r"E:\code\notes\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    # excel_path = r"D:\lvcode\noteOnGithub\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    file_name = r"D:\lvcode\noteOnGithub\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    sheet_name = "黄阁西互通"
    # eval_sentence = """loc[df["起讫桩号"]=="合计", '挖方总数量']"""
    skiprows = """2"""
    header = """[0, 1 ,2]"""
    # eval_sentence = """iloc[:, 0:2]"""
    eval_sentence = """loc[df["起点"]>2000, ['挖方总数量', '路线前缀']]"""
    # eval_sentence = """loc[df["起讫桩号"].str.contains("匝道"), '挖方总数量']"""
    data = get_sheet_data(file_name, sheet_name, eval_sentence, skiprows, header)
    print("data:", data)







