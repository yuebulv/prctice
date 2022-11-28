# coding:utf-8
'''
功能：检查excel数据间的相关关系是否满足要求
要求：数据间的相互关系可以方便灵活定义
'''
import pandas as pd
from pandas import DataFrame, Series
import sys


def check_rules():
    tf_km_sheet = [
        '''df[‘长度’]==df['起点']-df['止点']''',
        '''df[’挖方总数量‘]==df['挖方土方松土']+df['挖方土方普通土']+df['挖方土方硬土']+df['挖方石方软石']+df['挖方石方次坚石']+df['挖方石方坚石']'''
    ]
    return tf_km_sheet


def check_dataframe_data(data_df: DataFrame, rules_of_check):
    df = data_df.copy
    for check_rule in rules_of_check:
        check_rule_eval = eval(check_rule)
        print(check_rule, check_rule_eval)


def demo():
    sys.path.append(r'./road')
    from Road.excel_py.sheet_data_clean import clean_sheet_data
    from Road.excel_py.pd_read_excel_strengthen import read_excel_strengthen
    from Road.chain_age import start_end_chainage_split_df
    file_name = r"D:\lvcode\noteOnGithub\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    sheet_name = "黄阁西互通"
    eval_sentence = """loc[df["起点"]>2000, ['挖方总数量', '路线前缀']]"""
    skiprows = 2
    header = [0, 1, 2]
    data_df = read_excel_strengthen(file_name, sheet_name=sheet_name, skiprows=skiprows, header=header, usecols='A:AU', na_filter=0)
    data_df = clean_sheet_data(data_df)
    data_df = start_end_chainage_split_df(data_df)
    check_dataframe_data(data_df, check_rules())


if __name__ == '__main__':
    demo()