#公路项目数据结构
    # 一、key（桩号序号）   前一key（桩号序号） 桩号  无断链桩号road.setupChainageTable(prjname,prjpath)
        #1 查找纬地项目文件prj中3dr文件路径
        #2 提取3dr文件中桩号
            #？需要检查是否有重复桩号
        #3 装3dr中的桩号，存入数据表key中
    # 二、边坡表
        #1 根据给定边沟/排水沟特征，从3dr中选出边沟/排水沟，并记录到排水沟表drainageDitch中。findDrainageDitchFromLine
            # 根据给定的边沟/排水沟判定条件，从一条线line中找出边沟/排水沟
                # 边沟/排水沟判定条件，
                    # 1.判定条件
                    # 2.排除条件
    #边沟/排水沟表drainageDitch
        #key    左右侧 3dr中起始位置     线段个数   平距  高差     平距  高差...
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

if __name__ == "__main__":
    prjpath = r'F:\2020-10-14长寿支线\4-资料\王勇\K -12-16 - 副本\K.prj'
    prjname='长寿支线'
    # temp=road.setupChainageTable(prjname,prjpath)
    # temp=road.creatMysqlDrainageDitchTable(prjname)

    chainage='A180.00000 '

    conn = pymysql.connect(user="root", passwd="sunday")  # ,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)

    threedrpath=road.findXPathFromPrj(prjpath,'3dr')
    cross_sections=road.getCrossSectionOf3dr(threedrpath,chainage)
    for data in cross_sections:
        cross_section=re.split(r'\n',data)
        # text=re.split(r'\t',text_list[0])
        i=0
        for temp in cross_section:
            temp=temp.strip()
            if len(temp)>0:
                cross_section[i]=temp
                i=i+1
        drainage=road.findDrainageDitchFromLine(cross_section[1])
        print(drainage)
        sql='insert into drainageditch values(%s,%s,%s,%s)'
        insert = cursor.execute(sql, (cross_section[0], 1, int(drainage[0]), int(drainage[1])))

        # sql = 'insert into drainageditch values(%s,%s,%s,...%s)'

        # i=1
        # # 3 装3dr中的桩号，存入数据表key中
        # for key in keyslist:
        #     insert = cursor.execute(sql,(i,i-1,key,0))
        #     i=i+1

    cursor.close()
    conn.commit()
    conn.close()
    # drainageFilter = [['width1', 'height1', 'gradient1'], ['width2', 'height2', 'gradient2']]
    # print(len(drainageFilter[0]))
    # print(drainageFilter[0])
    #
    # res='  1.5 < h1 < 9999 '
    # res=res.replace(' ','')
    # print(res)
    # # print(float(res))



