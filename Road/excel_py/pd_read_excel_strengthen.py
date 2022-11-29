# coding:utf-8
import pandas as pd
import os


def read_excel_strengthen(io, sheet_name=0, *, header=0, names=None, index_col=None, usecols=None, squeeze=None,
                          dtype=None, engine=None, converters=None, true_values=None, false_values=None, skiprows=None,
                          nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False,
                          parse_dates=False, date_parser=None, thousands=None, decimal='.', comment=None, skipfooter=0,
                          convert_float=None, mangle_dupe_cols=True, storage_options=None):
    '''
    :param io:
    :param sheet_name:
    :param header:
    :param names:
    :param index_col:
    :param usecols:
    :param squeeze:
    :param dtype:
    :param engine:
    :param converters:
    :param true_values:
    :param false_values:
    :param skiprows:
    :param nrows: 读入前N行，N中不包含skiprows；即如果header占x行，data占Y行，X+Y=Nrows
    :param na_values:
    :param keep_default_na:
    :param na_filter:
    :param verbose:
    :param parse_dates:
    :param date_parser:
    :param thousands:
    :param decimal:
    :param comment:
    :param skipfooter:
    :param convert_float:
    :param mangle_dupe_cols:
    :param storage_options:
    :return:
    '''
    # try: 方法一：存在问题多层索引中合并单元格非首位值为空
    #     dataDf = pd.read_excel(io, sheet_name=sheet_name, skiprows=skiprows, na_filter=0, header=header, usecols=usecols, nrows=nrows)
    # except ValueError:
    #     dataDf = pd.read_excel(io, sheet_name=sheet_name, skiprows=skiprows, na_filter=0, header=None, usecols=usecols, nrows=nrows)
    #     dataDf_columns = dataDf.iloc[header, :] # 不能直接取列索引，否则合并单元格非首位值为空
    #     dataDf.drop(header, inplace=True)
    #     dataDf.columns = pd.MultiIndex.from_arrays(dataDf_columns.values)
    # return dataDf

    # 方法二
    try:
        dataDf = pd.read_excel(io, sheet_name=sheet_name, skiprows=skiprows, na_filter=0, header=header, usecols=usecols, nrows=nrows)
    except ValueError:
        dataDf = pd.read_excel(io, sheet_name=sheet_name, skiprows=skiprows, na_filter=0, header=None, usecols=usecols, nrows=nrows)
        # dataDf_columns = dataDf.iloc[header, :] # 不能直接取列索引，否则合并单元格非首位值为空
        dataDf.drop(header, inplace=True)

        dataDf_header = pd.read_excel(io, sheet_name=sheet_name, skiprows=skiprows, na_filter=0, header=header, nrows=0)
        dataDf_header_df = dataDf_header.columns.to_frame(index=False).T
        tem_path = os.path.dirname(io) + r'/tem_read_excel.xlsx'
        dataDf_header_df.to_excel(tem_path, header=False, index=False)
        dataDf_header_fillna = pd.read_excel(tem_path, usecols=usecols, header=None)
        os.remove(tem_path)
        # print(dataDf_header_fillna)
        # print(pd.MultiIndex.from_frame(dataDf_header_fillna))
        dataDf.columns = pd.MultiIndex.from_frame(dataDf_header_fillna.T)
    return dataDf