from Road.excel_py.road_excel_columns_port import *  # 不能删除
from Road.file_public.str_func import str_map_factory


class RoadExcel(object):
    def __init__(self, excel_name, excel_sheet=None):
        self.excel_name = excel_name
        self.excel_sheet = excel_sheet
        self.format_columns_class_and_excel_name_keys_dic = {
            'TfExcelFormatColumns()': [('土石方',)],
            'PsExcelFormatColumns()': [('排水', )],
            'RoadExcelFormatColumns()': [('',)],
        }  # 与road_excel_columns_port.py中类FormatColumns名称有耦合
        self.format_abbreviation_and_excel_name_keys_dic = {
            '每公里土石方': [('每公里土石方',)],
            '排水工程': [('排水工程',)],
            '防护': [('防护',)],
            '路面': [('路面工程',)],
            '涵洞': [('涵洞', '数量')],
            '特殊': [('特殊',)],
            '新旧': [('新旧',)],
            '夯实': [('夯实',)],
            '护栏': [('护栏',)],
            '用地': [('用地',)],
            '标志': [('标志',)],
            '青苗': [('青苗',)],
            '砍树': [('砍树',)],
            '技术指标': [('技术指标',)],
        }

    def get_format_columns(self):
        format_columns_class_and_excel_name_keys_dic = str_map_factory(self.excel_name, self.format_columns_class_and_excel_name_keys_dic)
        excel_format_columns_class = eval(format_columns_class_and_excel_name_keys_dic)
        excel_format_columns = excel_format_columns_class.columns
        return excel_format_columns

    def get_abbreviation_excel_name(self):
        abbreviation_excel_name = str_map_factory(self.excel_name, self.format_abbreviation_and_excel_name_keys_dic)
        return abbreviation_excel_name


def demo(column_str):
    # tf_excel_columns = TfExcelColumns()
    # format_column = tf_excel_columns.format_column(column_str)
    # return format_column

    # tf_excel_columns = TfExcelColumns()
    # return str_map_factory(tf_excel_columns.columns, column_str)

    excel_name = r'SZYS06010111 每公里土石方数量表汇总表.xls'
    # excel_name = r'路基、路面排水工程数量表.xls'
    excel_name = r'公路病害治理工程数量表'
    sheet_name = ''
    road_excel = RoadExcel(excel_name, sheet_name)
    road_excel_columns = road_excel.get_format_columns()
    format_column = str_map_factory(column_str, road_excel_columns)
    return format_column


if __name__ == '__main__':
    column_port = demo('zad')
    print(column_port)
    # str1 = '桩号'
    # str2 = '止点'
    # print(str2.find(str1))