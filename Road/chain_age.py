import re
import pandas as pd
from pandas import DataFrame, Series
import numpy as np


def start_end_chainage_split(start_end_chainage: str) -> list:
    # 例GAK36+086.363-GAK37+000，返回[36086.363, 37000, GA]
    res_list = ['', '', '']
    start_end_chainage = start_end_chainage.upper()
    if start_end_chainage.find('K') == -1:
        return res_list
    if start_end_chainage.find('+') == -1:
        return res_list
    regx = r"[-]*[\d+.]+"
    chain_list = re.findall(regx, start_end_chainage, re.MULTILINE)
    for i in range(0, len(chain_list)):
        res_list[i] = chain_list[i].replace("+", "")
    regx = r"[A-J|L-Z]+"
    try:
        road_name = re.findall(regx, start_end_chainage, re.MULTILINE)[0]
    except IndexError:
        road_name = ""
    res_list[-1] = road_name
    return res_list


def start_end_chainage_split_df(start_end_chainage_combined_df: DataFrame) -> DataFrame:
    '''根据列:起讫桩号,添加列：起点、止点、路线编号;输入输出都是DataFrame'''
    dataDf = start_end_chainage_combined_df
    try:
        start_end_chainage_split_df: DataFrame = dataDf["起讫桩号"].map(start_end_chainage_split) \
                                                .map(lambda x: ",".join(x)).str.split(",", expand=True)
    except KeyError:
        return dataDf
    start_end_chainage_split_df.replace("", np.nan, inplace=True)
    start_end_chainage_split_df.rename(columns={0: "起点", 1: "止点", 2: "路线前缀"}, inplace=True)
    dataDf[start_end_chainage_split_df.columns] = start_end_chainage_split_df
    dataDf['起点'] = dataDf['起点'].astype(float)
    dataDf['止点'] = dataDf['止点'].astype(float)
    return dataDf