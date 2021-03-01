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

def findDrainageDitchFromLine(linedata,drainageFilters='default'):
    #功能：根据给定的边沟/排水沟判定条件drainageFilters，从一条线linedata中找出边沟/排水沟，返回res=[6,3],表示linedata中第6段线开始为边沟/排水沟，边沟/排水沟由3条线段组成。
    #(linedata格式要像3dr左侧或右侧横断面格式，组数、平距、高差.....）
    #边沟/排水沟判定条件drainageFilters，格式应按程序默认值格式，width height gradient 为关键字，只接受小写；默认边沟/排水沟由3条线组成，每条线由width height gradient来判定
        #1.判定条件Filte
        #2.排除条件（目前未添加此功能）

    if drainageFilters=='default':
        drainageFilter1 = ['0<=width', 'height<0', '-1.5<=gradient<=0'] #第1条边判定条件
        drainageFilter2 = ['0<width', 'height<0.5', '5<abs(gradient)<=9999']    #第2条边判定条件
        drainageFilter3 = ['0<=width', '0<height', '0<=gradient<=1.5']  #第3条边判定条件
        Filter=[drainageFilter1,drainageFilter2,drainageFilter3]

    regx=r'-?\d*\.?\d+'
    pointsOfLinedata=re.findall(regx,linedata)
    # print(pointsOfLinedata)
    m=0
    i = 0
    res = []
    try:
        while i <float(pointsOfLinedata[0])-1:
            widthOfPoint=float(pointsOfLinedata[(i+2)*2-1])-float(pointsOfLinedata[(i+2-1)*2-1])
            widthOfPoint=abs(float('{:.3f}'.format(widthOfPoint)))
            heightOfPoint = float(pointsOfLinedata[(i + 2) * 2])-float(pointsOfLinedata[(i + 2-1) * 2])
            heightOfPoint=float('{:.3f}'.format(heightOfPoint))
            try:
                gradientOfPint=widthOfPoint/heightOfPoint
                gradientOfPint= float('{:.3f}'.format(gradientOfPint))
            except ZeroDivisionError:
                gradientOfPint=9999
            # print(widthOfPoint,heightOfPoint,gradientOfPint)
            [width, height, gradient] = [widthOfPoint, heightOfPoint, gradientOfPint]
            if eval(Filter[m][0]):
                i_last=i
                if eval(Filter[m][1]):
                    if eval(Filter[m][2]):
                        m=m+1
                        if m == len(Filter):    #判定为边沟/排水沟条件
                            res.append(i-len(Filter)+1)
                            res.append(len(Filter))
                            m = 0
                    else:
                        if m != 0:
                            i = i_last - 1
                            m = 0
                else:
                    if m!=0:
                        i = i_last - 1
                        m=0
            else:
                m=0
            i=i+1
        if len(res)!=0:
            return res
        else:
            return False
    except:
        return False



if __name__ == "__main__":
    prjpath = r'F:\2020-10-14长寿支线\4-资料\王勇\K -12-16 - 副本\K.3dr'

    chainage='  A180.00000 '
    cross_sections=road.getCrossSectionOf3dr(prjpath,chainage)
    for data in cross_sections:
        cross_section=re.split(r'\n',data)
        # text=re.split(r'\t',text_list[0])
        i=0
        for temp in cross_section:
            temp=temp.strip()
            if len(temp)>0:
                cross_section[i]=temp
                i=i+1

        res=findDrainageDitchFromLine(cross_section[1])
        print(res)

    # drainageFilter = [['width1', 'height1', 'gradient1'], ['width2', 'height2', 'gradient2']]
    # print(len(drainageFilter[0]))
    # print(drainageFilter[0])
    #
    # res='  1.5 < h1 < 9999 '
    # res=res.replace(' ','')
    # print(res)
    # # print(float(res))



