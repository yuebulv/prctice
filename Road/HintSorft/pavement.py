# coding=utf-8
from tkinter import *
import tkinter as tk
import tkinter.messagebox
import os
import pymysql
import road as road
import mysql as mysql
import copy
from roadglobal import ljTitle_dic
import roadglobal
from operator import itemgetter
import sys
import numpy as np
import mysql_py
# from ..file_public import getData_list


def creatMysqlPavementTable(databaseName):
    # 在databaseName数据库中新建边坡表Pavement
    # 桩号	左右侧	路面结构类型	路基宽度	路肩处与地面高差	中央分隔带宽度	土路肩宽度	硬路肩宽度	路面宽度	新建宽度	原路利用宽度	原路上加铺宽度	原路上加铺厚度
    # lj	lj	    手动	        lj	    计算	            lj	         lj     	lj      	lj  	手动  	手动      	手动      	手动
    tablename = 'pavement'
    prjname = databaseName
    conn = pymysql.connect(user="root", passwd="sunday")  # ,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)
    cursor.execute(f'drop table if exists {tablename}')
    sql = """CREATE TABLE IF NOT EXISTS `pavement` (
          `id` int(6) NOT NULL,
          `chainage` varchar(50) NOT NULL ,
          `左右侧` int(1) NOT NULL ,
          `路面结构类型` varchar(50) ,
          `路肩端部填/挖` float(10) ,
          `半幅中分隔带宽度` float(10) ,
          `行车道宽度` float(10) ,
          `硬路肩宽度` float(10) ,
          `土路肩宽度` float(10) ,
          `新建宽度` float(10) ,
          `原路利用宽度` float(10) ,
          `原路上加铺宽度` float(10),
          `原路上加铺厚度` float(10),
           PRIMARY KEY (`id`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    print('pavement表创建成功V1.0')


def insertDataFromLjToTablePavement(lj_path, prjname):
    # 只能识别纬地lj文件，是否可以识别不同软件数据
    databaseName = prjname
    if not os.path.exists(lj_path):
        return f"insertDataFromLjToTablePavement:{lj_path}文件不存在"

    # 2.导入纬地.lj中对应数据
    lj_data_list = road.getDataFromTf(lj_path, chainage='all')
    for i in range(len(lj_data_list)):
        lj_data_list[i] = re.findall(r'\S+', lj_data_list[i], re.MULTILINE)
    lj_data_np = np.array(lj_data_list)  # 转为二维数组
    lj_data_np_1 = lj_data_np[:, 0]
    lj_data_np_2 = np.delete(lj_data_np, 0, 1)
    lj_data_np_2 = np.asarray(lj_data_np_2, dtype=float)
    lj_data_np = np.insert(lj_data_np_2, 0, lj_data_np_1, axis=1)

    # pavementData_for_table = np.empty((len(lj_data_list)*2, 13), dtype=object)
    pavementData_for_table = np.zeros((len(lj_data_list)*2, 13), dtype=object)
    pavementData_for_table[:, 0] = range(len(lj_data_list)*2)
    pavementData_for_table[:, 1] = np.concatenate((lj_data_np[:, ljTitle_dic['桩号']-1], lj_data_np[:, ljTitle_dic['桩号']-1]), axis=0)
    l_or_r_list = [1]*len(lj_data_list)
    l_or_r_list.extend([2]*len(lj_data_list))
    pavementData_for_table[:, 2] = l_or_r_list
    pavementData_for_table[:, 5] = np.concatenate((lj_data_np[:, ljTitle_dic['左半幅中分带宽度']-1], lj_data_np[:, ljTitle_dic['右半幅中分带宽度']-1]), axis=0)
    pavementData_for_table[:, 6] = np.concatenate((lj_data_np[:, ljTitle_dic['左侧行车道宽度']-1] + lj_data_np[:, ljTitle_dic['左侧引用车道宽度']-1],
                                                   lj_data_np[:, ljTitle_dic['右侧行车道宽度']-1] + lj_data_np[:, ljTitle_dic['右侧引用车道宽度']-1]), axis=0)
    pavementData_for_table[:, 7] = np.concatenate((lj_data_np[:, ljTitle_dic['左侧硬路肩宽度']-1], lj_data_np[:, ljTitle_dic['右侧硬路肩宽度']-1]), axis=0)
    pavementData_for_table[:, 8] = np.concatenate((lj_data_np[:, ljTitle_dic['左侧土路肩宽度']-1], lj_data_np[:, ljTitle_dic['右侧土路肩宽度']-1]), axis=0)
    pavementData_for_table = pavementData_for_table.tolist()

    # 3.将路面数据pavementData_for_table存入数据库中
    # conn = pymysql.connect(user="root", passwd="sunday")  # 方法一
    # cursor = conn.cursor()
    # conn.select_db(databaseName)
    # for pavementData in pavementData_for_table:
    #     sql = "insert into pavement values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #     insert = cursor.execute(sql, pavementData)
    # cursor.close()
    # conn.commit()
    # conn.close()
    # print("路面宽度信息已存入pavement表")
    sql = "insert into pavement values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    insert_massage = mysql_py.insertDataToMysql(databaseName, sql, pavementData_for_table)
    print(insert_massage)


def cal_dmx_elevation():
    pass


def outputPavement(prjname, prjpath, slopefilepath):
    '''
    功能:输出分组路面段落及必要参数
    :param slopefilepath:结果保存路径
    :return:结果存入slopefilepath文件中
    '''
    print(slopefilepath)
    outputslopefile = open(slopefilepath, 'w')

    fieldList = ['左右侧', '路面结构类型']  # 将fieldList中字段（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldMax = []  # 寻找fieldMax中字段的最大值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldMin = []  # 寻找fieldMin中字段的最小值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldSum = [2, '行车道宽度', '硬路肩宽度', '路面面积',
                '(((行车道宽度)+(硬路肩宽度))+((行车道宽度_last)+(硬路肩宽度_last)))/2*lenOfchainage']
    field_list = [fieldMax, fieldMin, fieldSum, fieldList]

    # with mysql.UsingMysql(log_time=False, db=prjname) as um:  # 数据表settheprotectiongtypeofslope中获取防护类型
    #     sql = f"select 防护类型 from settheprotectiongtypeofslope "
    #     um.cursor.execute(sql)
    #     slopeprotypeInTable_list_dic = um.cursor.fetchall()
    # slopeprotypeInTable_list = [item[key] for item in slopeprotypeInTable_list_dic for key in item]
    for lorR_slope in [1, 2]:
        # for lorR_slope_drainage in [1, 2]:
        #     for protype in slopeprotypeInTable_list:
        #         for slopelevel in range(1, roadglobal.slopelevel_max):  # 指定边坡最大8级
        sql = f'''
                        SELECT chainage.id id_chainage,slope.坡高,pavement.*
                        FROM slope,pavement,chainage
                        where slope.坡高<0 AND pavement.左右侧={lorR_slope} and pavement.路面结构类型=0
                        AND slope.chainage=chainage.chainage
                        ORDER BY id_chainage ASC;'''
        slopedata_res = road.groupByContinuousChainageAndSum(prjname, sql, prjpath, field_list)
        print(f'outputSlopeRange({prjname}, {prjpath}, {slopefilepath}),slopedata_res:{slopedata_res}')
        try:
            outputslopefile.write(str(list(slopedata_res[0].keys())))
            outputslopefile.write('\n')
        except:
            pass
        for temp in slopedata_res:
            road.insert_dic_data_to_table(prjname, roadglobal.tableName_of_slopeInGroup, temp)
            outputslopefile.write(str(list(temp.values())))
            outputslopefile.write('\n')
            print(temp.values())
    outputslopefile.close()
    print(f'{slopefilepath}输出成功！')


def main():
    databaseName = "k_小坎互通"
    prjpath = r'F:\20230417G85银昆高速、G93成渝地区环线高速重庆高新区至荣昌区（川渝界）段改扩建工程施工图勘察设计（一标段）\1互通纬地数据\20230602开放设计\20230602数据融合\K\K.PRJ'
    slopefilepath = r'F:\20230417G85银昆高速、G93成渝地区环线高速重庆高新区至荣昌区（川渝界）段改扩建工程施工图勘察设计（一标段）\1互通纬地数据\20230602开放设计\20230602数据融合\K\pave.txt'
    lj_path = road.findXPathFromPrj(r'F:\20230417G85银昆高速、G93成渝地区环线高速重庆高新区至荣昌区（川渝界）段改扩建工程施工图勘察设计（一标段）\1互通纬地数据\20230602开放设计\20230602数据融合\K\K.PRJ', 'lj')

    # 1.创建pavement表
    creatMysqlPavementTable(databaseName)

    # 2.导入纬地.lj中对应数据
    insertDataFromLjToTablePavement(lj_path, databaseName)

    # 3.分组输出路面数量
    outputPavement(databaseName, prjpath, slopefilepath)


if __name__ == "__main__":
    main()
