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


def switchBreakChainageToNoBreak(chainage,prjpath):
    '''
    :param chainage:
    :param pathOfCtr:
    :return:chainage(无断链)(float)或者返回''
    '''
    try:
        chainage=chainage.strip().upper()
    except:
        chainage=str(chainage)
    pathOfCtr=prjpath
    if len(chainage)>0:
        chainage=road.cutInvalidWords_chainage(chainage)
        if len(chainage[0]) == 0:
            return float(chainage[1])
        if 65<=ord(chainage[0])<=90:
            pass
        else:
            return float(chainage[1])
        try:
            ctrfile=open(pathOfCtr,'r')
        except:
            msgbox = road.gui_filenotfine(f'{pathOfCtr}文件不存在')
            sys.exit()
        else:
            ctrfileData=ctrfile.read()
            ctrfile.close()
            regx = r'断链.+=(.+=.+)'
            breakchainsInCtr=re.findall(regx,ctrfileData,re.MULTILINE)
            # print(f'breakchainInCtr:{breakchainsInCtr}')
            if len(breakchainsInCtr)>0:
                breakchain_list=[]
                for breakchainInCtr in breakchainsInCtr:
                    breakchain=breakchainInCtr.split('=')
                    breakchain_list.append(breakchain)
                    # print(f'breakchain_list:{breakchain_list}')
                correctionsOfChainage=0
                for i in range(0,ord(chainage[0])-65):
                    correctionsOfChainage=correctionsOfChainage+float(breakchain_list[i][0].strip())-float(breakchain_list[i][1].strip())
                # print(f'correctionsOfChainage:{correctionsOfChainage}')
                # print(chainage[1])
                chainage_nobreak=float(chainage[1])+correctionsOfChainage
                return chainage_nobreak
            else:
                return float(chainage[1])
    else:
        return ''

    
def switchNoBreakToBreakChainage(chainage,prjpath):
    '''
    :param chainage:
    :param pathOfCtr:
    :return:chainage(含断链)(float)或者返回''
    '''
    try:
        chainage=chainage.strip().upper()
    except:
        chainage=str(chainage)
    pathOfCtr=prjpath
    if len(chainage)>0:
        # chainage=road.cutInvalidWords_chainage(chainage)
        # if 65<=ord(chainage[0])<=90:
        #     pass
        # else:
        #     return chainage[1]
        try:
            ctrfile=open(pathOfCtr,'r')
        except:
            msgbox = road.gui_filenotfine(f'{pathOfCtr}文件不存在')
            sys.exit()
        else:
            ctrfileData=ctrfile.read()
            ctrfile.close()
            regx = r'断链.+=(.+=.+)'
            breakchainsInCtr=re.findall(regx,ctrfileData,re.MULTILINE)
            # print(f'breakchainInCtr:{breakchainsInCtr}')
            if len(breakchainsInCtr)>0:
                breakchain_list=[]
                chainage_actual = {}
                chainage_Chain_before = {}
                chainage_Chain_next = {}
                for breakchainInCtr in breakchainsInCtr:
                    breakchain=breakchainInCtr.split('=')
                    breakchain_list.append(breakchain)
                    # print(f'breakchain_list:{breakchain_list}')
                correctionsOfChainage = 0
                chainage_actual[0] = float(breakchain_list[0][0].strip())
                chainage_Chain_next[0] = float(breakchain_list[0][1].strip())
                i = 0
                for i in range(1, len(breakchain_list)):
                    correctionsOfChainage = correctionsOfChainage+float(breakchain_list[i-1][0].strip())-float(breakchain_list[i-1][1].strip())
                    chainage_actual[i] = float(breakchain_list[i][0].strip()) + correctionsOfChainage
                    chainage_Chain_before[i] = float(breakchain_list[i][0].strip())
                    chainage_Chain_next[i] = float(breakchain_list[i][1].strip())
                # print(f'correctionsOfChainage:{correctionsOfChainage}')
                # print(chainage[1])
                # print(f'chainage_actual[i]:{chainage_actual}')
                while float(chainage) < chainage_actual[i]:
                    i = i - 1
                    if i<0:
                        return chr(i+66) + str(round(float(chainage),3))
                # print(i)
                chainage = chainage_Chain_next[i] + float(chainage) - chainage_actual[i]
                chainage_break = chr(i+66) + str(round(chainage,3))
                return chainage_break
            else:
                return chainage
    else:
        return ''