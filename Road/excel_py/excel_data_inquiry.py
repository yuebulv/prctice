# coding:utf-8
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
import sys
import xlwings as xw
import os
from Road.excel_py.road_excel import *


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


def tf_km_sheet_data(eval_sentence):

    return eval(eval_sentence)


@xw.func
@xw.ret(index=False, expand='table')
def inquiry_excel_data(eval_sentence, file_name, sheet_name, skiprows=None, header="0", usecols=None, sheet_type="road", nrows=None):
    '''
    :param file_name:要查询文件的路径+文件名
    :param sheet_name:要查询表格name
    :param eval_sentence:执行的查询语句,如"""loc[df["起讫桩号"]=="合计", '挖方总数量']"""，不需要在前面加df.
    :param skiprows:需要忽略前N行，int
    :param header:表头所在行，例"""[0, 1 ,2]"""，从skiprow之后开始计
    :param sheet_type:如果为road,则运行函数start_end_chainage_split_df（根据起讫桩号添加列：起点、止点、路线编号）
    :param usecols:
    :return:
    '''
    from Road.excel_py.sheet_data_clean import clean_sheet_data as sheet_data_clean
    from Road.excel_py.pd_read_excel_strengthen import read_excel_strengthen
    skiprows = eval(str(skiprows))
    header = eval(header)
    # try:
    #     dataDf = pd.read_excel(file_name, sheet_name=sheet_name, skiprows=skiprows, na_filter=0, header=header, usecols=usecols)
    # except ValueError:
    #     dataDf = pd.read_excel(file_name, sheet_name=sheet_name, skiprows=skiprows, na_filter=0, header=None, usecols=usecols)
    #     dataDf_columns = dataDf.iloc[header, :]
    #     dataDf.drop(header, inplace=True)
    #     dataDf.columns = pd.MultiIndex.from_arrays(dataDf_columns.values)
    dataDf = read_excel_strengthen(file_name, sheet_name=sheet_name, skiprows=skiprows, na_filter=0, header=header, usecols=usecols, nrows=nrows)
    # df: DataFrame = sheet_data_clean(file_name, sheet_name, skiprows, header)
    df: DataFrame = sheet_data_clean(dataDf)
    if sheet_type.lower() == 'road':
        # 格式化df中的列标签
        from Road.file_public.str_func import str_map_factory
        # from Road.excel_py.road_excel import *
        excel_name = os.path.basename(file_name)
        road_excel = RoadExcel(excel_name)
        road_format_columns = road_excel.get_format_columns()
        df.columns = pd.Series(list(df.columns)).apply(str_map_factory, map_dic=road_format_columns)

        # moudle_path = os.path.abspath(r'..')  # 引入包
        # sys.path.insert(0, moudle_path)
        from Road.chain_age import start_end_chainage_split_df
        df = start_end_chainage_split_df(df)
    res = eval("df" + "." + eval_sentence)
    return res.values


def alias_of_file(file_name_str) -> str:
    # 给文件取别名
    # sys.path.append(r'./road')
    from Road.file_public.str_func import getNumofCommonSubstr
    alias_str = '排水工程，防护，路面，每公里,涵洞，特殊，新旧，夯实，用地，护栏，标志，青苗，砍树，技术指标'
    alias = getNumofCommonSubstr(file_name_str, alias_str)
    return alias[0]


@xw.func
def output_road_contents_excel(project_path):
    # 功能：得到project_path路径下所有的excel[文件名, 别名，文件路径，工作表1，工作表n]，保存位置project_path + r"\road_content.xlsx"
    from Road.file_public.file_public import get_contents_excel
    path_str = project_path
    contents_df = get_contents_excel(path_str=path_str)
    try:
        contents_df['file_alias'] = contents_df['file_name'].map(alias_of_file)  # 给文件增加别名
    except KeyError:
        pass
    contents_df_columns_list = list(contents_df.columns)
    contents_df_columns_list.remove('file_name')
    contents_df_columns_list.remove('file_alias')
    new_columns = ['file_name', 'file_alias']
    new_columns.extend(contents_df_columns_list)
    contents_df = contents_df[new_columns]
    path_str = project_path + r"\road_content.xlsx"
    contents_df.to_excel(path_str)


def demo():
    # 1. output_road_contents_excel(project_path),输出项目下所有excel表名，路径等。非必须步骤
    # 2. get_sheet_data(eval_sentence, file_name, sheet_name, skiprows, header) 查询数据
    # 3. 其中file_name，可以在excel文件调用步骤1 中结果，简化。
    # project_path = r'F:\20211124长寿农村道路\1-CAD\20221128电厂路-起点段不加宽'
    # output_road_contents_excel(project_path)

    # file_name = r"E:\code\notes\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    file_name = r"D:\lvcode\noteOnGithub\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    sheet_name = "黄阁西互通"
    eval_sentence = """loc[df["起讫桩号"]=="合计", '清表回填']"""
    # eval_sentence = """iloc[:, 0:2]"""
    # eval_sentence = """loc[df["起讫桩号"].str.contains("匝道"), '挖方总数量']"""
    # eval_sentence = """loc[df["起点"]>2000, ['挖方总数量', '路线前缀']]"""
    skiprows = 2
    header = """[0, 1 ,2]"""
    usecols = 'A:AU'
    nrows = 67

    # file_name = r'F:\20211124长寿农村道路\1-CAD\20221128电厂路-起点段不加宽\S-17路基土石方汇总数量表.xls'
    # sheet_name = '土石方汇总'
    # eval_sentence = '''loc[df["桩号"].str.contains("计", na=False),:]'''
    # skiprows = 2
    # header = """[0, 1 ,2, 3]"""
    # usecols = 'A:X'
    # nrows = 20
    data = inquiry_excel_data(eval_sentence, file_name, sheet_name, skiprows, header, usecols=usecols, nrows=nrows)
    print(type(data))
    print("data:", data)


if __name__ == "__main__":
    # tf = TfSheet("path", "columns", "chain")
    # tf.get_tf_data()
    demo()








