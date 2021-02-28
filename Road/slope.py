#公路项目数据结构
    # 一、key（桩号序号）   前一key（桩号序号） 桩号  无断链桩号road.setupChainageTable(prjname,prjpath)
        #1 查找纬地项目文件prj中3dr文件路径
        #2 提取3dr文件中桩号
            #？需要检查是否有重复桩号
        #3 装3dr中的桩号，存入数据表key中
    # 二、边坡表
        #1 根据给定边沟/排水沟特征，从3dr中选出边沟/排水沟，并记录到排水沟表drainageDitch中
            # 根据给定的边沟/排水沟判定条件，从一条线line中找出边沟/排水沟
                # 边沟/排水沟判定条件，
                    # 1.判定条件
                    # 2.排除条件
    # 	key（桩号序号）   左右侧	边坡类型（填挖） 坡高 最大级数    【第i级平台	第i级平台坡度	第i级平台平距	第i级平台高度	第i级平台坐标x	第i级平台坐标y	第i级平台高程
                                                        # 	第i级边坡	第i级边坡坡度	第i级边坡平距	第i级边坡高度	第i级边坡坐标x	第i级边坡坐标y	第i级边坡高程】

    #防护类型表（根据防护通用图）
    #     防护类型 条件1 条件2....
    # 将边坡数据导入数据库
    # SQL根据数据库中边坡数据、防护类型表确定各断面边坡采用的防护类型
import TransEiDatToHint3dr
from tkinter import *
import tkinter as tk
import os
import road
import pymysql
import math

def FindDrainageDitchFromLine(linedata,drainageFilter):
    #根据给定的边沟/排水沟判定条件，从一条线linedata中找出边沟/排水沟，如从3dr中断面左侧数据中找出边沟/排水沟位置,(linedata格式要像3dr左侧或右侧横断面格式，组数、平距、高差.....）
    #边沟/排水沟判定条件，drainageFilter
        #1.判定条件
        #2.排除条件
    drainageFilter=[['width1','height1','gradient1'],['width2','height2','gradient2'],['width3','height3','gradient3']]
    regx=r'\d+\.?\d+'
    res=re.findall(regx,linedata,re.MULTILINE)
    for i in range[len(drainageFilter),len(res[0])]:
        print(i)

if __name__ == "__main__":
    prjpath = r'F:\2020-10-14长寿支线\4-资料\王勇\K -12-16 - 副本\K.3dr'

    chainage='  A80.00000 '
    cross_sections=road.getCrossSectionOf3dr(prjpath,chainage)
    for data in cross_sections:
        cross_section=re.split(r'\n',data)
        # text=re.split(r'\t',text_list[0])
        for temp in cross_section:
            temp=temp.strip()

            print(temp)

    # drainageFilter = [['width1', 'height1', 'gradient1'], ['width2', 'height2', 'gradient2']]
    # print(len(drainageFilter[0]))
    # print(drainageFilter[0])