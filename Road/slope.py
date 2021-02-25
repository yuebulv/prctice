#公路项目数据结构
    # 一、key（桩号序号）   前一key（桩号序号） 桩号  无断链桩号
        #1 查找纬地项目文件prj中3dr文件路径
        #2 提取3dr文件中桩号
        #3 装3dr中的桩号，存入数据表key中
    # 二、边坡表
    # 	key（桩号序号）	边坡类型（填挖） 坡高 最大级数    【第i级平台	第i级平台坡度	第i级平台平距	第i级平台高度	第i级平台坐标x	第i级平台坐标y	第i级平台高程
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

if __name__=="__main__":
    prjname='长寿支线'
    prjpath=r'F:\2020-10-14长寿支线\4-资料\王勇\K -12-16 - 副本\K.PRJ'
    temp=road.setupChainageTable(prjname,prjpath)
