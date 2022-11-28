# coding:utf-8
import pandas as pd


def read_excel_strengthen(io, sheet_name=0, *, header=0, names=None, index_col=None, usecols=None, squeeze=None,
                          dtype=None, engine=None, converters=None, true_values=None, false_values=None, skiprows=None,
                          nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False,
                          parse_dates=False, date_parser=None, thousands=None, decimal='.', comment=None, skipfooter=0,
                          convert_float=None, mangle_dupe_cols=True, storage_options=None):
    try:
        dataDf = pd.read_excel(io, sheet_name=sheet_name, skiprows=skiprows, na_filter=0, header=header, usecols=usecols)
    except ValueError:
        dataDf = pd.read_excel(io, sheet_name=sheet_name, skiprows=skiprows, na_filter=0, header=None, usecols=usecols)
        dataDf_columns = dataDf.iloc[header, :]
        dataDf.drop(header, inplace=True)
        dataDf.columns = pd.MultiIndex.from_arrays(dataDf_columns.values)
    return dataDf