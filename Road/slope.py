'''
#公路项目数据结构
    # 一、key（桩号序号）   前一key（桩号序号） 桩号  无断链桩号road.setupChainageTable(prjname,prjpath)
        #1 查找纬地项目文件prj中3dr文件路径
        #2 提取3dr文件中桩号
            #？需要检查是否有重复桩号
        #3 装3dr中的桩号，存入数据表key中
    # 二、确定边沟/排水沟范围（默认一个3dr断面单侧最多有一条边沟或排水沟）
        #1 根据给定边沟/排水沟特征，从3dr中选出边沟/排水沟，并记录到排水沟表drainageDitch中。insertDataToTableDrainageDitchFrom3dr
            # 根据给定的边沟/排水沟判定条件，从一条线line中找出边沟/排水沟 findDrainageDitchFromLine
                # 边沟/排水沟判定条件，
                    # 1.判定条件
                    # 2.排除条件
        #边沟/排水沟表drainageDitch
            #序号 chainage    左右侧 3dr中起始位置     线段个数   平距  高差     平距  高差...
    #三、确定平台、边坡范围
        注：路肩与边沟/排水沟之间线段判断为边坡
        #1 根据TF文件中路基边缘为起始点，
        #2 边坡分类
            #1）位于路基边缘与边沟/排水沟之间A
                #1.1 下坡为填方  （判断填方最后一级是否为护坡道，第一级也有可能是平台）
                    #1.1.1 B为上坡
                    #1.1.2 B为下坡
                    #1.1.3 B为0
                #1.2 上坡为挖方（情况可以忽略）
            #2）位于边沟/排水沟与坡脚之间B
                # 2.1 下坡为填方  （判断填方第一级是否为平台）
                    # 2.1.1 A为上坡
                    # 2.1.2 A为下坡
                    # 2.1.3 A为0
                # 2.2 上坡为挖方（第一级有可能为平台）
                    # 2.2.1 A为上坡
                    # 2.2.2 A为下坡
                    # 2.2.3 A为0
        边坡表slope
            #序号 chainage    左右侧(1/2) 位于边沟左右侧(0(无边沟)/1（边沟左侧）/2（边沟右内里）)	边坡类型（1填-1挖） 坡高 最大级数    【第i级平台	第i级平台坡度	第i级平台平距	第i级平台高度	第i级平台坐标x	第i级平台坐标y	第i级平台高程
                                                                                                                    # 	第i级边坡	第i级边坡坡度	第i级边坡平距	第i级边坡高度	第i级边坡坐标x	第i级边坡坐标y	第i级边坡高程】


    #防护类型表（根据防护通用图）
    #     防护类型 条件1 条件2....
    # 将边坡数据导入数据库
    # SQL根据数据库中边坡数据、防护类型表确定各断面边坡采用的防护类型
'''

import TransEiDatToHint3dr
from tkinter import *
import tkinter as tk
import os
import road
import pymysql
import math
import mysql

if __name__ == "__main__":
    prjpath = r'F:\2020-10-14长寿支线\4-资料\王勇\K -12-16 - 副本\K.prj'
    # prjpath = r'D:\Download\QQ文档\297358842\FileRecv\元蔓纬地设计文件\元蔓纬地设计文件\K27改移老路调坡上报\K27+400改移地方道路.prj'
    prjname='长寿支线'
    # #一、 生成数据表chainage
    # road.setupChainageTable(prjname,prjpath)
    # road.creatMysqlDrainageDitchTable(prjname)
    chainages=['all']
    chainage='a0'
    # for chainage in chainages:
    #     # 二、 生成数据表DrainageDitchTable
    #     threedrpath = road.findXPathFromPrj(prjpath, '3dr')
    #     temp_insert = road.insertDataToTableDrainageDitchFrom3dr(threedrpath, chainage, prjname)

    try:
        chainage=road.getChainageFromChainagetable(prjname,chainage,True)[0]    #返回数据表chainage中等值桩号
    except:
        print('桩号错误')
    else:
        tfpath = road.findXPathFromPrj(prjpath, 'tf')
        tfDatas=road.getDataFromTf(tfpath,chainage)     #得到TF数据
        for tfData_temp in tfDatas:
            regx=r'\w+.?\w+'
            tfData=re.findall(regx,tfData_temp,re.MULTILINE)
            print(tfData[0],tfData[4],tfData[5])
            # print(len(tfData))
            # print(tfData)
        with mysql.UsingMysql(log_time=False,db=prjname) as um:     #得到边沟数据
            um.cursor.execute(f"select chainage,左右侧,3dr中起始位置  from drainageditch where chainage='{chainage}'")
            data = um.cursor.fetchall()
            print(data)
    road.creatMysqlSlopeTable(prjname)







