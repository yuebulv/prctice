from Road.excel_py.road_excel_columns_port import *  # 不能删除
from Road.excel_py.road_excel_check_rules import *  # 不能删除
from Road.file_public.str_func import str_map_factory
from pandas import DataFrame
import pandas as pd
import os


class RoadExcel(object):
    def __init__(self, excel_name, excel_sheet=None):
        self.excel_name = excel_name
        self.excel_sheet = excel_sheet
        self.format_columns_class_and_excel_name_keys_dic = {
            'TfExcelFormatColumns()': [('土石方',)],
            'PsExcelFormatColumns()': [('排水工程', )],
            'FhExcelFormatColumns()': [('防护', )],
            'QbExcelFormatColumns()': [('耕地', )],
            'QtExcelFormatColumns()': [('桥头', )],
            'XjExcelFormatColumns()': [('新旧', )],
            'QlExcelFormatColumns()': [('桥梁', )],
            'RoadExcelFormatColumns()': [('',)],
        }  # 与road_excel_columns_port.py中类FormatColumns名称有耦合
        self.check_rules_function_and_excel_name_map_dic = {
            'RoadTfExcelCheckRules()': [('土石方',)],
            'RoadProtectExcelCheckRules()': [('防护',)],
            'RoadDrainExcelCheckRules()': [('排水工程',)],
            'RoadPavingExcelCheckRules()': [('路面工程',)],
            'RoadExcelFormatColumns()': [('',)],
        }  # 与road_excel_check_rules.py中类RoadExcelCheckRules名称有耦合
        self.data_df: DataFrame

    def get_format_columns(self):
        format_columns_class_and_excel_name_keys_dic = str_map_factory(self.excel_name, self.format_columns_class_and_excel_name_keys_dic)
        excel_format_columns_class = eval(format_columns_class_and_excel_name_keys_dic)
        excel_format_columns = excel_format_columns_class.columns
        return excel_format_columns

    def get_abbreviation_excel_name(self):
        from Road.excel_py.road_excel_settings import format_abbreviation_and_excel_name_keys_dic
        abbreviation_excel_name = str_map_factory(self.excel_name, format_abbreviation_and_excel_name_keys_dic)
        return abbreviation_excel_name

    def get_excel_data(self, *args, **kwargs):
        from Road.excel_py.pd_read_excel_strengthen import read_excel_strengthen
        from Road.excel_py.sheet_data_clean import clean_sheet_data
        from Road.chain_age import start_end_chainage_split_df
        data_df = read_excel_strengthen(*args, **kwargs)
        data_df = clean_sheet_data(data_df)
        # 格式化df中的列标签
        road_format_columns = self.get_format_columns()
        data_df.columns = pd.Series(list(data_df.columns)).apply(str_map_factory, map_dic=road_format_columns)

        data_df = start_end_chainage_split_df(data_df)
        self.data_df = data_df
        return data_df

    def check_dataframe_data(self, data_df: DataFrame, output_file):
        # check_rule格式{'exp': '检查用的表达式', 'columns': [结果中输出的columns列], 'rexg': '如果columns为空[]时，刚用正则划分columns'}
        import re
        import numpy as np
        check_rules_function_str = str_map_factory(self.excel_name, self.check_rules_function_and_excel_name_map_dic)
        check_rules_class = eval(check_rules_function_str)
        rules_of_check = check_rules_class.check_rules
        df = data_df.copy()

        # df.astype('float64')
        df.replace(np.nan, 0, inplace=True)
        # for col_index in df.iteritems():
        #     pd.to_numeric(df[col_index], errors='ignore')
        from Road.file_public.str_func import value_to_numeric
        df = df.applymap(value_to_numeric)
        # print(f'df_type:{df.dtypes}')
        # print(df.head())
        for check_rule in rules_of_check:
            if not check_rule['columns']:
                check_rule['columns'] = re.split(check_rule['regx'], check_rule['exp'])
            check_rule['columns'] = [_ for _ in check_rule['columns'] if _ in list(df.columns)]
            # print(f'check_rule:{check_rule}')
            res_df = df.query(check_rule['exp'])[check_rule['columns']]
            if res_df.empty:
                continue
            if not os.path.exists(output_file):
                res_df.to_excel(output_file)
                continue
            with pd.ExcelWriter(path=output_file, mode='a') as writer:
                res_df.to_excel(writer)


def demo(column_str):
    excel_name = r'SZYS06010111 每公里土石方数量表汇总表.xls'
    # excel_name = r'路基、路面排水工程数量表.xls'
    excel_name = r'公路病害治理工程数量表'
    sheet_name = ''
    road_excel = RoadExcel(excel_name, sheet_name)
    road_excel_columns = road_excel.get_format_columns()
    format_column = str_map_factory(column_str, road_excel_columns)
    return format_column


def check_demo():
    file_name = r"D:\lvcode\noteOnGithub\noteOnGithub\data\SZYS06010111 每公里土石方数量表汇总表.xls"
    sheet_name = "黄阁西互通"
    skiprows = 2
    header = [0, 1, 2]
    nrow = 67
    # data_df = read_excel_strengthen(file_name, sheet_name=sheet_name, skiprows=skiprows, header=header, usecols='A:AU', na_filter=0)
    # data_df = clean_sheet_data(data_df)
    # data_df = start_end_chainage_split_df(data_df)
    # output_path = os.path.dirname(file_name) + r'\check_out.xlsx'
    # check_dataframe_data(data_df, check_rules(), output_path)

    tf_sheet = RoadExcel(file_name, sheet_name)
    tf_sheet.get_excel_data(file_name, sheet_name, skiprows=skiprows, header=header, usecols='A:AU', na_filter=0, nrows=nrow)
    output_file_name = os.path.basename(file_name) + r'_check_out.xlsx'
    output_path = os.path.join(os.path.dirname(file_name), output_file_name)
    # output_path = os.path.dirname(file_name) + r'\check_out.xlsx'
    tf_sheet.check_dataframe_data(tf_sheet.data_df, output_path)


if __name__ == '__main__':
    # column_port = demo('zad')
    # print(column_port)

    check_demo()