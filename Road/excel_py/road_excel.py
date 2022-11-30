from Road.excel_py.road_excel_columns_port import *
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

    def get_format_columns(self):
        format_columns_class_and_excel_name_keys_dic = str_map_factory(self.excel_name, self.format_columns_class_and_excel_name_keys_dic)
        excel_format_columns_class = eval(format_columns_class_and_excel_name_keys_dic)
        excel_format_columns = excel_format_columns_class.columns
        return excel_format_columns


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