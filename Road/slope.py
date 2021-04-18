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
            #序号 chainage    左右侧(1/2) 位于边沟左右侧(0(无边沟)/1（边沟左侧）/2（边沟右内里）)	边坡类型（1填-1挖） 坡高 最大级数
                【第i级平台	第i级平台坡度	第i级平台平距	第i级平台高度	第i级平台坐标x	第i级平台坐标y	第i级平台高程
                第i级边坡	    第i级边坡坡度	第i级边坡平距	第i级边坡高度	第i级边坡坐标x	第i级边坡坐标y	第i级边坡高程】
            注：边坡类型 填-1 挖1 分离式填方-11 分离式挖方11
    四、查询分组合并输出边坡表
        4.1 桥梁桩号处理
            4.1.1 分左右幅
            4.1.2 标注桥梁
            4.1.3 端点处理
        4.2 断链处理
            4.2.1 含断链桩号与无断链桩桩号相互转换
    五、防护类型表（根据防护通用图）
        5.1 边坡防护类型相关因素
            坡度 坡高 本级高度 第i级 共i级 地质
            防护类型 条件1 条件2....
        编写边坡sql
            SQL根据数据库中边坡数据、防护类型表确定各断面边坡采用的防护类型
        编写挡墙sql
            路肩墙
            路中墙
            路堤墙
            护肩
            护脚
            无法区分直立边坡是挡墙还是分离式路基处理
        5.3 输出桩号范围限定?s
    六、排水

    regx 全局变量
'''

import TransEiDatToHint3dr
from tkinter import *
import tkinter as tk
import os
import road
import pymysql
import math
import mysql
import copy
import glob
# import filedialog
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    folderpath = filedialog.askdirectory(title='请选择prj文件所在文件夹')
    os.chdir(folderpath)
    for prjfile in glob.glob('*.prj'):
        prjpath = folderpath+'\\'+prjfile
        if os.path.exists(prjpath) == False:
            msgbox = road.gui_filenotfine(f'{prjpath} path:不在存在')
            continue
        prjpath = prjpath.replace('/', '\\')
        slopefilepath_list = prjpath.split('\\')
        regx = r'(.+)(?=\.\w+)'
        prjname = re.findall(regx, slopefilepath_list[-1])[0]
        prjname = prjname.replace('+', '')
        # print(prjname)

        #一、 生成数据表chainage
        road.setupChainageTable(prjname, prjpath)
        road.creatMysqlDrainageDitchTable(prjname)
        with mysql.UsingMysql(log_time=False, db=prjname) as um:
            sql = f"select chainage from chainage "
            um.cursor.execute(sql)
            chainageValuesInTable_list_dic = um.cursor.fetchall()
        chainageValuesInTable_list = [item[key] for item in chainageValuesInTable_list_dic for key in item]
        chainages = chainageValuesInTable_list

        # 二、 生成数据表DrainageDitchTable
        for chainage in chainages:
            threedrpath = road.findXPathFromPrj(prjpath, '3dr')
            temp_insert = road.insertDataToTableDrainageDitchFrom3dr(threedrpath, chainage, prjname)
        # 三、新建数据表slope，并导入数据
        road.creatMysqlSlopeTable(prjname)
        for chainage in chainages:
            road.insertDataFrom3drToTableSlope(prjpath, chainage, prjname)
        road.creatMysqlSlopeProtecTypeTable(prjname)

        # 四、输出分组边坡段落及必要参数
        regx = r'(.+)(?=\.\w+)'
        prjfilename = re.findall(regx, slopefilepath_list[-1])
        slopefilename = f'{prjfilename[0]}{prjname}slopedata.txt'
        slopefilepath_list[-1] = slopefilename
        slopefilepath = '\\'.join(slopefilepath_list)
        print(slopefilepath)
        outputslopefile = open(slopefilepath, 'w')

        fieldList = ['左右侧', '第i级', 'S坡度', '位于边沟左右侧', '防护类型']  # 将fieldList中字段（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
        fieldMax = ['最大级数', '坡高']  # 寻找fieldMax中字段的最大值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
        fieldMin = ['坡高']  # 寻找fieldMin中字段的最小值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
        fieldSum = [2, 'S宽度', 'S高度', '坡面面积',
                    '(((S宽度)**2+(S高度)**2)**0.5+((S宽度_last)**2+(S高度_last)**2)**0.5)/2*lenOfchainage']
        field_list = [fieldMax, fieldMin, fieldSum, fieldList]

        with mysql.UsingMysql(log_time=False, db=prjname) as um:    #数据表settheprotectiongtypeofslope中获取防护类型
            sql = f"select 防护类型 from settheprotectiongtypeofslope "
            um.cursor.execute(sql)
            slopeprotypeInTable_list_dic = um.cursor.fetchall()
        slopeprotypeInTable_list = [item[key] for item in slopeprotypeInTable_list_dic for key in item]
        for lorR_slope in [1, 2]:
            for lorR_slope_drainage in [1, 2]:
                for protype in slopeprotypeInTable_list:
                    for slopelevel in range(1, 8):   # 指定边坡最大8级
                        sql = f'''
                                SELECT chainage.id id_chainage,slope.*,sp.防护类型
                                FROM slope,settheprotectiongtypeofslope sp,chainage
                                where slope.边坡类型<3 AND slope.左右侧={lorR_slope} and slope.位于边沟左右侧={lorR_slope_drainage} AND `第i级`={slopelevel}
                                AND slope.chainage=chainage.chainage
                                AND slope.第i级 BETWEEN SP.第i级min AND sp.第i级max
                                AND slope.S坡度 BETWEEN SP.坡度min AND sp.坡度max
                                AND slope.最大级数 BETWEEN sp.最大级数min And sp.最大级数max
                                AND slope.`S高度` BETWEEN sp.高度min And sp.高度max
                                AND slope.`坡高` BETWEEN sp.坡高min And sp.坡高max
                                AND sp.`防护类型`='{protype}'
                                ORDER BY id_chainage ASC;'''
                        # fieldList = ['左右侧', '第i级', 'S坡度', '位于边沟左右侧', '防护类型']  # 将fieldList中字段（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
                        # fieldMax = ['最大级数', '坡高']  # 寻找fieldMax中字段的最大值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
                        # fieldMin = ['坡高']  # 寻找fieldMin中字段的最小值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
                        # fieldSum = [2, 'S宽度', 'S高度', '坡面面积',
                        #             '(((S宽度)**2+(S高度)**2)**0.5+((S宽度_last)**2+(S高度_last)**2)**0.5)/2*lenOfchainage']
                        # field_list = [fieldMax, fieldMin, fieldSum, fieldList]
                        slopedata_res = road.groupByContinuousChainageAndSum(prjname, sql, prjpath, field_list)
                        try:
                            outputslopefile.write(str(list(slopedata_res[0].keys())))
                            outputslopefile.write('\n')
                        except:
                            pass
                        for temp in slopedata_res:
                            outputslopefile.write(str(list(temp.values())))
                            outputslopefile.write('\n')
                            print(temp.values())
        outputslopefile.close()
        print(f'{slopefilepath}输出成功！')

        # 五、输出分组排水沟段落及必要参数
        regx = r'(.+)(?=\.\w+)'
        prjfilename = re.findall(regx, slopefilepath_list[-1])
        slopefilename = f'{prjfilename[0]}{prjname}drainagedata.txt'
        slopefilepath_list[-1] = slopefilename
        slopefilepath = '\\'.join(slopefilepath_list)
        print(slopefilepath)
        outputslopefile = open(slopefilepath, 'w')

        fieldList = ['左右侧', '边坡类型']  # 将fieldList中字段（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
        fieldMax = ['坡高']  # 寻找fieldMax中字段的最大值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
        fieldMin = ['坡高']  # 寻找fieldMin中字段的最小值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
        fieldSum = []
        field_list = [fieldMax, fieldMin, fieldSum, fieldList]
        drainTypeSql_list =[['slope.坡高>0', 'slope.`位于边沟左右侧`=2'], ['slope.坡高<0', 'slope.`位于边沟左右侧`=1']]
        for drainTypeSql in drainTypeSql_list:
            for lorR_drain in [1, 2]:
                sql = f'''
                    SELECT 
                        chainage.id id_chainage,dr.chainage,any_value(slope.`边坡类型`) 边坡类型,any_value(slope.`坡高`) `坡高`,dr.`左右侧`
                    FROM 
                        drainageditch dr
                    JOIN 
                        chainage
                    on 
                        dr.chainage=chainage.chainage
                    left JOIN
                        slope
                    on 
                        dr.chainage=slope.chainage
                    AND
                        dr.`左右侧`=slope.`左右侧`
                    where 
                        dr.左右侧={lorR_drain}
                    AND
                        slope.`边坡类型`<3
                    AND
                        {drainTypeSql[0]}
                    AND
                        {drainTypeSql[1]}
                    GROUP BY
                        chainage.id
                    ORDER BY 
                        id_chainage ASC;'''

                slopedata_res = road.groupByContinuousChainageAndSum(prjname, sql, prjpath, field_list)
                try:
                    outputslopefile.write(str(list(slopedata_res[0].keys())))
                    outputslopefile.write('\n')
                except:
                    pass
                for temp in slopedata_res:
                    outputslopefile.write(str(list(temp.values())))
                    outputslopefile.write('\n')
                    print(temp.values())
        outputslopefile.close()
        print(f'{slopefilepath}输出成功！')