# coding:utf-8
'''
功能：检查excel数据间的相关关系是否满足要求
要求：数据间的相互关系可以方便灵活定义
'''
import pandas as pd
from pandas import DataFrame, Series
import sys
import os


# def check_rules():
#     # check_rule格式{'exp': '检查用的表达式', 'columns': [结果中输出的columns列], 'rexg': '如果columns为空[]时，刚用正则划分columns'}
#     tf_km_sheet = [
#         {'exp': '止点<=起点', 'columns': ['起点', '止点'], 'regx': r'[^\+\-*\/=\!\'\"\s]+'},
#         {'exp': '长度!=止点-起点', 'columns': ['长度', '起点', '止点']},
#         {'exp': '挖方总数量!=挖方土方松土+挖方土方普通土+挖方土方硬土+挖方石方软石+挖方石方次坚石+挖方石方坚石', 'columns': [], 'regx': r'[\+\-\*\/\=\!\'\"\s]+'},
#         {'exp': '填方总数量!=填方土方+填方石方', 'columns': ['填方总数量', '填方土方', '填方石方']},
#      ]
#     return tf_km_sheet
#
#
# def check_dataframe_data(data_df: DataFrame, rules_of_check, output_file):
#     # check_rule格式{'exp': '检查用的表达式', 'columns': [结果中输出的columns列], 'rexg': '如果columns为空[]时，刚用正则划分columns'}
#     import re
#     df = data_df.copy()
#     for check_rule in rules_of_check:
#         if not check_rule['columns']:
#             check_rule['columns'] = re.split(check_rule['regx'], check_rule['exp'])
#         res_df = df.query(check_rule['exp'])[check_rule['columns']].head()
#         if res_df.empty:
#             continue
#         if not os.path.exists(output_file):
#             res_df.to_excel(output_file)
#             continue
#         with pd.ExcelWriter(path=output_file, mode='a') as writer:
#             res_df.to_excel(writer)
#         # print(f'res_df:{res_df}')
#
#
# def demo():
#     sys.path.append(r'./road')
#     from Road.excel_py.sheet_data_clean import clean_sheet_data
#     from Road.excel_py.pd_read_excel_strengthen import read_excel_strengthen
#     from Road.chain_age import start_end_chainage_split_df
#     import os
#     file_name = r"D:\lvcode\noteOnGithub\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
#     sheet_name = "黄阁西互通"
#     eval_sentence = """loc[df["起点"]>2000, ['挖方总数量', '路线前缀']]"""
#     skiprows = 2
#     header = [0, 1, 2]
#     data_df = read_excel_strengthen(file_name, sheet_name=sheet_name, skiprows=skiprows, header=header, usecols='A:AU', na_filter=0)
#     data_df = clean_sheet_data(data_df)
#     data_df = start_end_chainage_split_df(data_df)
#     output_path = os.path.dirname(file_name) + r'\check_out.xlsx'
#     check_dataframe_data(data_df, check_rules(), output_path)
#     # rules = '长度!=止点-起点'
#     # print(data_df.query(rules)[['长度', '起点', '止点']])
#
#
# if __name__ == '__main__':
#     demo()