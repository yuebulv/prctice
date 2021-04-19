#road 常用函数
from tkinter import *
import tkinter as tk
import tkinter.messagebox
import os
import pymysql
import road
import mysql
import copy
import roadglobal
def outputPlatformdrainRange(prjname, prjpath, slopefilepath):
    '''
    功能:输出分组平台截水沟段落及必要参数
    :param slopefilepath:结果保存路径
    :return:['起点', '止点', '长度', '左右侧', '位于边沟左右侧', '第i级', 'P坡度', 'P宽度max', 'P宽度min']
    结果存入slopefilepath文件中
    '''
    print(slopefilepath)
    outputslopefile = open(slopefilepath, 'w')

    fieldList = ['左右侧', '位于边沟左右侧', '第i级', 'P坡度']  # 将fieldList中字段（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldMax = ['P宽度']  # 寻找fieldMax中字段的最大值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldMin = ['P宽度']  # 寻找fieldMin中字段的最小值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldSum = []
    field_list = [fieldMax, fieldMin, fieldSum, fieldList]

    drainTypeSql_list = [['slope.坡高>=0', 'slope.`位于边沟左右侧`=2'], ['slope.坡高<0', 'slope.`位于边沟左右侧`=1']]
    for lorR_drain in [1, 2]:
        for drainTypeSql in drainTypeSql_list:
            for slopelevel in range(1, roadglobal.slopelevel_max):
                sql = f'''
                        SELECT 
                            chainage.id id_chainage,slope.chainage,slope.`左右侧`,slope.坡高,slope.`第i级`,slope.`P宽度`,slope.`P坡度`,slope.`位于边沟左右侧`
                        FROM 
                            slope,chainage
                        WHERE chainage.chainage=slope.chainage
                        AND 
                            slope.`P宽度`>0
                        AND 
                            slope.`左右侧`={lorR_drain}
                        AND 
                            slope.第i级={slopelevel}
                       AND
                           {drainTypeSql[0]}
                       AND
                           {drainTypeSql[1]}
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

def outputSlopeRange(prjname, prjpath, slopefilepath):
    '''
    功能:输出分组边坡段落及必要参数
    :param slopefilepath:结果保存路径
    :return:结果存入slopefilepath文件中
    '''
    print(slopefilepath)
    outputslopefile = open(slopefilepath, 'w')

    fieldList = ['左右侧', '第i级', 'S坡度', '位于边沟左右侧', '防护类型']  # 将fieldList中字段（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldMax = ['最大级数', '坡高']  # 寻找fieldMax中字段的最大值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldMin = ['坡高']  # 寻找fieldMin中字段的最小值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldSum = [2, 'S宽度', 'S高度', '坡面面积',
                '(((S宽度)**2+(S高度)**2)**0.5+((S宽度_last)**2+(S高度_last)**2)**0.5)/2*lenOfchainage']
    field_list = [fieldMax, fieldMin, fieldSum, fieldList]

    with mysql.UsingMysql(log_time=False, db=prjname) as um:  # 数据表settheprotectiongtypeofslope中获取防护类型
        sql = f"select 防护类型 from settheprotectiongtypeofslope "
        um.cursor.execute(sql)
        slopeprotypeInTable_list_dic = um.cursor.fetchall()
    slopeprotypeInTable_list = [item[key] for item in slopeprotypeInTable_list_dic for key in item]
    for lorR_slope in [1, 2]:
        for lorR_slope_drainage in [1, 2]:
            for protype in slopeprotypeInTable_list:
                for slopelevel in range(1, roadglobal.slopelevel_max):  # 指定边坡最大8级
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

def outputDrainRange(prjname, prjpath, slopefilepath):
    '''
    功能:输出分组排水沟段落及必要参数
    :param slopefilepath:结果保存路径
    :return:结果存入slopefilepath文件中
    '''
    outputslopefile = open(slopefilepath, 'w')

    fieldList = ['左右侧', '边坡类型']  # 将fieldList中字段（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldMax = ['坡高']  # 寻找fieldMax中字段的最大值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldMin = ['坡高']  # 寻找fieldMin中字段的最小值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
    fieldSum = []
    field_list = [fieldMax, fieldMin, fieldSum, fieldList]
    drainTypeSql_list = [['slope.坡高>0', 'slope.`位于边沟左右侧`=2'], ['slope.坡高<0', 'slope.`位于边沟左右侧`=1']]
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

def groupByContinuousChainageAndSum(prjname, sql, prjpath, field_list = 'default'):
    '''
    功能：将sql查询结果，分组输出
    :param prjname:
    :param sql:
    :param field_list:
    :param prjpath:
    :return:res=[res_dic],{起点，止点，长度，field_list中字段}
        注意：1，平均断面法在求面积时，计算长度lenOfchainage在曲线处时不是两相邻桩号之差，曲线内侧是lenOfchainage会偏小，反之偏大；
        2，相邻桩号高度不同时，计算的平均高度与总体图中相比偏小；（比如总体图中平台在两端会延伸与地面线相交后，形成一条折线）
        3，头部增加一行起点数据（计算得，尺寸与后一断面一致），尾部增加一行起点数据（计算得，尺寸与前一断面一致），以修正输出结果的起止点和数量，数量可能比实际大
    '''
    groupdata_list = []
    if field_list == 'default':
        fieldList = ['左右侧', '第i级', 'S坡度', '位于边沟左右侧']   # 将fieldList中字段（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
        fieldMax = ['最大级数', '坡高']   # 寻找fieldMax中字段的最大值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
        fieldMin = ['坡高']   # 寻找fieldMin中字段的最小值（必须与sql结果中字段对应）在结果中列出，可扩展[字段1，字段2]
        fieldSum = [2, 'S宽度', 'S高度', '坡面面积', '(((S宽度)**2+(S高度)**2)**0.5+((S宽度_last)**2+(S高度_last)**2)**0.5)/2*lenOfchainage']  # 按计算式fieldSum[-1]（计算式名称：坡面面积）累加，2表示有两个参数，即计算式fieldSum[-1]有两个参数，暂时不可扩展
        field_list = [fieldMax, fieldMin, fieldSum, fieldList]
    res_dic = {'起点': '', '止点': '', '长度': ''}
    with mysql.UsingMysql(log_time=False, db=prjname) as um:
        um.cursor.execute(sql)
        mysqldatas = um.cursor.fetchall()
        # print(mysqldatas)
        # print(len(mysqldatas))
        # print(type(mysqldatas))
        # 一、按数据表chainage中的id（id_chainage）是否连续分组
        if isinstance(mysqldatas, dict):    # 只有一个桩号
            groupdata_list.append([mysqldatas])
        elif isinstance(mysqldatas, list):    # 多个桩号
            for i in range(0, len(mysqldatas)):
                # print(mysqldatas[i]['chainage'])
                if i == 0:
                    groupdata_list.append([mysqldatas[i]])
                    continue
                if mysqldatas[i]['id_chainage']-1 == mysqldatas[i-1]['id_chainage']:
                    groupdata_list[-1].append(mysqldatas[i])
                else:
                    groupdata_list.append([mysqldatas[i]])
                # print(mysqldatas[i])
    #二、按field_list中关键字段输出res_dic，起点、止点、长度为默认输出字段，
        res = []
        for groupdata_dic_list in groupdata_list:
            # print(f'groupdata_dic_list:{groupdata_dic_list}')
            # 2.0在groupdata_dic_list头部增加一行起点数据（计算得），尾部增加一行起点数据（计算得），以修正输出结果的起止点和数量
            groupdata_dic_list.insert(0, copy.deepcopy(groupdata_dic_list[0]))  #重点，必须用deepcopy
            groupdata_dic_list.append(copy.deepcopy(groupdata_dic_list[-1]))
            for i_addchainage in [0,-1]:
                if i_addchainage == 0:
                    id_chainage = groupdata_dic_list[i_addchainage]['id_chainage']-1
                else:
                    id_chainage = groupdata_dic_list[i_addchainage]['id_chainage'] + 1
                sql=f'''SELECT chainage FROM chainage WHERE ID ={id_chainage};'''
                um.cursor.execute(sql)
                chainageA_dic = um.cursor.fetchone()
                try:
                    chainageA = chainageA_dic['chainage']
                except:
                    chainageA = groupdata_dic_list[i_addchainage]['chainage']
                chainageB = groupdata_dic_list[i_addchainage]['chainage']
                # print(f'chainageA:{chainageA}')
                # print(f'chainageB:{chainageB}')
                chainage_new = road.findBridgeChainageFromABChainage(chainageA, chainageB, prjpath, groupdata_dic_list[i_addchainage]['左右侧'])
                # print(f'chainage_new:{chainage_new}')
                # print(i_addchainage)
                # print(groupdata_dic_list)
                groupdata_dic_list[i_addchainage]['chainage'] = chainage_new
                # print(groupdata_dic_list)
                # for i_field_sum in range(0, int(field_list[2][0])):     # 修改参与数量计算参数为0,修改为0后起止点数量偏小，所以头尾新增断面尺寸暂时与其相邻断面一致；
                #     groupdata_dic_list[i_addchainage][field_list[2][1+i_field_sum]] = 0
            # print(f'groupdata_dic_list,add new chainage:{groupdata_dic_list}')
            del res_dic
            res_dic = {}
            fieldofsumparameter = {}
            fieldofsumparameter_last = {}
            # 2.1 计算起点、止点、长度
            res_dic['起点'] = groupdata_dic_list[0]['chainage']
            res_dic['止点'] = groupdata_dic_list[-1]['chainage']
            lastchainage = road.switchBreakChainageToNoBreak(groupdata_dic_list[0]['chainage'], prjpath)
            lenOfchainage = road.switchBreakChainageToNoBreak(groupdata_dic_list[-1]['chainage'], prjpath)
            lenOfchainage = lenOfchainage - lastchainage
            res_dic['长度'] = round(lenOfchainage, 3)
            # 2.2 计算fieldList中字段值
            for field in field_list[3]:
                res_dic[field] = groupdata_dic_list[0][field]
            # 2.3 计算[fieldMax, fieldMin, fieldSum]中字段值
            for groupdata_dic in groupdata_dic_list:

                try:
                    field_list[0]
                except IndexError:
                    pass
                else:
                    for field_max in field_list[0]:
                        try:
                            res_dic[field_max+'max'] = max(groupdata_dic[field_max], res_dic[field_max+'max'])
                        except KeyError:
                            res_dic[field_max+'max'] = groupdata_dic[field_max]
                        res_dic[field_max + 'max'] = round(res_dic[field_max+'max'], 3)
                try:
                    field_list[1]
                except IndexError:
                    pass
                else:
                    for field_min in field_list[1]:
                        try:
                            res_dic[field_min+'min'] = min(groupdata_dic[field_min], res_dic[field_min+'min'])
                        except KeyError:
                            res_dic[field_min+'min'] = groupdata_dic[field_min]
                        res_dic[field_min + 'min'] = round(res_dic[field_min+'min'], 3)

                chainage = road.switchBreakChainageToNoBreak(groupdata_dic['chainage'], prjpath)
                lenOfchainage = chainage - lastchainage

                # 2.3.1计算[fieldSum]中字段值
                try:
                    sumexpression = field_list[2][-1]
                except IndexError:
                    pass
                else:
                    for i_field_sum in range(0, int(field_list[2][0])):
                        fieldofsumparameter[i_field_sum] = str(groupdata_dic[field_list[2][i_field_sum+1]])
                        try:
                            fieldofsumparameter_last[i_field_sum]
                        except KeyError:
                            fieldofsumparameter_last[i_field_sum] = fieldofsumparameter[i_field_sum]
                        sumexpression = sumexpression.replace(field_list[2][i_field_sum + 1] + '_last', fieldofsumparameter_last[i_field_sum])
                        sumexpression = sumexpression.replace(field_list[2][i_field_sum+1], fieldofsumparameter[i_field_sum])
                        # print(f'field_list[2][-1]:{field_list[2][-1]}')
                        # print(f'field_list[2][i_field_sum+1]:{field_list[2][i_field_sum+1]}')
                        fieldofsumparameter_last[i_field_sum] = fieldofsumparameter[i_field_sum]
                    print(sumexpression)
                    print(lenOfchainage)
                    try:
                        res_dic[field_list[2][-2]] += eval(sumexpression)
                        print(eval(sumexpression))
                    except KeyError:
                        res_dic[field_list[2][-2]] = eval(sumexpression)
                        print(eval(sumexpression))

                lastchainage = chainage
            try:
                res_dic[field_list[2][-2]] = "{:+.3f}".format(res_dic[field_list[2][-2]])
            except:
                pass
            res.append(res_dic)
            print(res_dic)
        return res
        # print(f'groupdata_list:{groupdata_list}')
        # print("-- 当前数量: %d " % len(mysqldatas))


def isbridgeOrTunnel(chainage, prjpath, lOrRSideOfsubgrade=1):
    '''
    功能：判断chainage路基类型，3表示桥梁、4表示隧道、否则为‘’
    :param chainage:
    :param pathOfCtr:
    :param lOrRSideOfsubgrade:1表示左幅路基，2表示右幅路基，
    :return:3/4/''
    '''
    pathOfCtr = road.findXPathFromPrj(prjpath, 'ctr')
    try:
        ctrfile = open(pathOfCtr,'r')
    except:  # except FileNotFoundError:
        # msgbox = road.gui_filenotfine(f'{pathOfCtr}ctr文件不存在')
        msgbox = tkinter.messagebox.askyesno('警告', f'{pathOfCtr}ctr文件不存在，是否继续', )
        if msgbox:
            return ''
        else:
            sys.exit()
    else:
        ctrFileData = ctrfile.read().upper()
        ctrfile.close()
        regx_qh = r'QHSJ\.DAT([\s|\S]+)HDSJ\.DAT'                                                         #软条件，随ctr格式变化
        regx_sd = r'SUIDAO\.DAT([\s|\S]+)SHUIZHUNDIAN\.DAT'
        regx_list = [regx_qh, regx_sd]
        i = 3
        for regx in regx_list:
            qhdatas = re.findall(regx, ctrFileData, re.MULTILINE)
            # print(f'qhdatas:{qhdatas}')
            for qhdata in qhdatas:
                qhs_list = qhdata.split('\n')
                # print(qhs_list)
                for qh in qhs_list:
                    regx = r'\S+'
                    qh_list = re.findall(regx, qh, re.MULTILINE)
                    # print(qh_list)
                    if len(qh_list) > 2:
                        qhChain_l = road.switchBreakChainageToNoBreak(qh_list[0], prjpath)
                        qhChain_n = road.switchBreakChainageToNoBreak(qh_list[1], prjpath)
                        chainage_nobreak = road.switchBreakChainageToNoBreak(chainage, prjpath)
                        if qhChain_l <= chainage_nobreak <= qhChain_n:
                            if i == 3:   # 左右幅判断(根据ctr中A桥梁所在行的最后一位判断-1左幅、1右幅、0整幅)
                                if float(qh_list[-1]) == 0:
                                    return i
                                elif float(qh_list[-1]) == -1 and float(lOrRSideOfsubgrade) == 1:
                                    return i
                                elif float(qh_list[-1]) == 1 and float(lOrRSideOfsubgrade) == 2:
                                    return i
                            else:
                                return i
                    else:
                        continue
            i = i + 1
        return ''
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
def insertDataToTableDrainageDitchFrom3dr(pathOf3dr,chainage,prjname):
    #功能：将3dr中桩号为chainage边沟/排水沟信息插入到DrainageDitch表中
    # road.getCrossSectionOf3dr得到3dr中桩号chainagea横断面数据
    # findDrainageDitchFromLine找出边沟/排水沟信息
    # 将边沟/排水沟信息存到数据库prjname表drainageditch中
    threedrpath=pathOf3dr
    conn = pymysql.connect(user="root", passwd="sunday")  # ,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)
    cross_sections=road.getCrossSectionOf3dr(threedrpath,chainage)
    for data in cross_sections:
        cross_section=re.split(r'\n',data)
        i=0
        for temp in cross_section:
            temp=temp.strip()
            if len(temp)>0:
                cross_section[i]=temp
                i=i+1
        for i_LOrR in [1,2]:
            drainage=road.findDrainageDitchFromLine(cross_section[i_LOrR])
            # print(i_LOrR,cross_section[0])
            # print(drainage)
            if drainage!=False:
                sql="insert into drainageditch(chainage,左右侧,3dr中起始位置,线段个数) values(%s,%s,%s,%s)"
                insert = cursor.execute(sql, (cross_section[0], i_LOrR, int(drainage[0]), int(drainage[1])))
                for i_drainage in range(int(drainage[1])):
                    sql = f'update drainageditch set 宽度{i_drainage}={float(drainage[i_drainage*3 + 2])} where chainage ="{cross_section[0]}" and 左右侧={i_LOrR}'
                    update_drain = cursor.execute(sql)
                    sql = f'update drainageditch set 高度{i_drainage}={float(drainage[i_drainage*3 + 3])} where chainage ="{cross_section[0]}" and 左右侧={i_LOrR}'
                    update_drain = cursor.execute(sql)
                    sql = f'update drainageditch set 坡度{i_drainage}={float(drainage[i_drainage*3 + 4])} where chainage ="{cross_section[0]}" and 左右侧={i_LOrR}'
                    update_drain=cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    print(f"桩号{chainage}边沟/排水沟信息已存入drainageditch表")
def insertDataFrom3drToTableSlope(prjpath, chainage, prjname):
    '''
    功能：将3dr中桩号为chainage边坡信息插入slope表中
    :param prjpath: 项目路径
    :param chainage: 桩号
    :param prjname: 项目名称
    :return:在数据库prjname数据表slope中生成桩号chainage的边坡信息
    方法：
        一、得到TF数据
        二、得到边沟数据
        三、根据路肩和边沟位置确定边坡范围
            1、第i级边坡+第i级平台组成一组数据（缺失部件时用0补齐）
            2、边坡可分为：1）路肩与边沟之间边坡；2）边沟与坡脚之间边坡
    '''

    try:
        chainage = road.getChainageFromChainagetable(prjname, chainage, True)[0]  # 返回数据表chainage中等值桩号
    except:
        print(f'错误：数据表chainage中无桩号{chainage}')
        return ''

    # 一、得到TF数据
    tfpath = road.findXPathFromPrj(prjpath, 'tf')
    tfDatas = road.getDataFromTf(tfpath, chainage)
    for tfData_temp in tfDatas:
        regx = r'\w+.?\w+'
        tfData = re.findall(regx, tfData_temp, re.MULTILINE)
        # print(tfData[0], tfData[4], tfData[5])
    try:
        len(tfData)
    except:
        print(f'TF文件中不存在桩号{chainage}')
        return ''
    # 二、得到边沟数据
    with mysql.UsingMysql(log_time=False, db=prjname) as um:
        um.cursor.execute(f"select chainage,左右侧,3dr中起始位置,线段个数  from drainageditch where chainage='{chainage}'")
        drainagedataFromtable = um.cursor.fetchall()
        # for dic in drainagedataFromtable:
        #     print(dic['左右侧'],dic['3dr中起始位置'])
        print('drainagedataFromtable', drainagedataFromtable)

    # 三、得到边坡数据
    threedrpath = road.findXPathFromPrj(prjpath, '3dr')
    conn = pymysql.connect(user="root", passwd="sunday")  # ,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)
    cross_sections = road.getCrossSectionOf3dr(threedrpath, chainage)
    for data in cross_sections:
        cross_section = re.split(r'\n', data)
        i = 0
        #3.1取得3dr数据
        for temp in cross_section:
            temp = temp.strip()
            if len(temp) > 0:
                cross_section[i] = temp
                i = i + 1
        # for slopePostionComparedWithdrainage in [1, 2]:  # 1表示边坡在边沟左侧，2表示边坡在边沟右侧
        for i_LOrR in [1, 2]:  # 左右侧
            roadShoulderPosition=''
            drainagePosition=''
            drainageLinesCount=''
            regx = r'-?\d+\.?\d*'
            drData_list = re.findall(regx, cross_section[i_LOrR], re.MULTILINE)
            print(f'cross_section[{i_LOrR}]:{cross_section[i_LOrR]}')
            print('drData_list', drData_list)
            #3.2确定路肩位置
            for i_drData_list in range(1, len(drData_list), 2):
                print(f'tfData{[i_LOrR + 3]}:{tfData[i_LOrR + 3]}')
                print(float(drData_list[i_drData_list]))
                if abs(float(tfData[i_LOrR + 3])) == abs(float(drData_list[i_drData_list])):
                    roadShoulderPosition = (i_drData_list - 3) / 2  # 默认TF文件中第4、5列为路基左、右宽度
                    print(f'tfdata{i_LOrR + 3}列在cross_section{i_LOrR}中的位置：第', roadShoulderPosition, '组')
                    break
            # 3.3确定边沟位置
            for drainagePosition_dic in drainagedataFromtable:
                if drainagePosition_dic['左右侧'] == i_LOrR:
                    drainagePosition = drainagePosition_dic['3dr中起始位置']
                    drainageLinesCount = drainagePosition_dic['线段个数']
                    print(f'边沟在3dr中的起始位置{i_LOrR}侧：第', drainagePosition, f'组；边沟线段个数:{drainageLinesCount}')
                    continue
                # else:   #不含边沟、排水沟时，边坡计入填方
                #     drainagePosition = int(drData_list[0]) - 1
                #     drainageLinesCount = 0
            try:
                i_slopeStart = roadShoulderPosition + 1
            except:
                print(f'桩号{chainage}中{i_LOrR}侧3dr中未找到土路肩宽度')
                continue
            try:    #不含边沟、排水沟时，边坡计入填方
                i_slopeEnd = drainagePosition+1
            except:
                drainagePosition =int(drData_list[0])-1
                drainageLinesCount =0
            print('roadShoulderPosition', roadShoulderPosition)
            # 3.4 1）路肩与边沟之间边坡；2）边沟与坡脚之间边坡 范围划分
            for slopePostionComparedWithdrainage in [1, 2]:  # 1表示边坡在边沟左侧，2表示边坡在边沟右侧
                if slopePostionComparedWithdrainage == 1:
                    i_slopeStart = roadShoulderPosition + 1
                    i_slopeEnd = drainagePosition
                else:
                    i_slopeStart = drainageLinesCount + drainagePosition
                    i_slopeEnd = int(drData_list[0]) - 1
                print(f'i_slopeStart{i_slopeStart},i_slopeEnd{i_slopeEnd},drainageLinesCount{drainageLinesCount}')
                slopeDatasFrom3dr = findSlopeFromLine(cross_section[i_LOrR], i_slopeStart, i_slopeEnd)
                print('findSlopeFromLine函数返回值', slopeDatasFrom3dr)

                #3.5 将数据插入数据表slope
                if len(slopeDatasFrom3dr) > 0:
                    slopeType = road.isbridgeOrTunnel(chainage, prjpath, i_LOrR)
                    if slopeType == '':
                        slopeType = 0
                    maxSlopelevel = slopeDatasFrom3dr[-1][1]
                    if slopeDatasFrom3dr[-1][4] == 0:   # 如果最后一级边坡坡比为0，则认为是分离式路基，边坡级数减-
                        maxSlopelevel = maxSlopelevel-1
                    for slopedata in slopeDatasFrom3dr:
                        slopedataForTable = [0, cross_section[0], i_LOrR, i_slopeStart, int(i_slopeEnd - i_slopeStart),
                                             slopePostionComparedWithdrainage, slopeType, slopedata[0], maxSlopelevel]
                        slopedataForTable = slopedataForTable + slopedata[1:]
                        sql = "insert into slope values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        # print(slopedataForTable)
                        insert = cursor.execute(sql, slopedataForTable)
    cursor.close()
    conn.commit()
    conn.close()
    print("边坡信息已存入drainageditch表")
def findBridgeChainageFromABChainage(chainageA, chainageB, prjpath, lOrRSideOfsubgrade=1):
    # 功能：已知两相邻桩号A/B，查找A/B之间是否存在桥隧起止点，如有返回桥隧起止桩号，否则返回中间桩号（A+B）/2
    # A/B为含断链桩号
    pathOfCtr = road.findXPathFromPrj(prjpath, 'ctr')
    try:
        ctrfile = open(pathOfCtr, 'r')
    except:  # except FileNotFoundError:
        msgbox = road.gui_filenotfine(f'{pathOfCtr}文件不存在')
        sys.exit()
    else:
        ctrFileData = ctrfile.read().upper()
        ctrfile.close()
        regx_qh = r'QHSJ\.DAT([\s|\S]+)HDSJ\.DAT'  # 软条件，随ctr格式变化
        regx_sd = r'SUIDAO\.DAT([\s|\S]+)SHUIZHUNDIAN\.DAT'
        regx_list = [regx_qh, regx_sd]
        i = 3
        for regx in regx_list:
            qhdatas = re.findall(regx, ctrFileData, re.MULTILINE)
            # print(f'qhdatas:{qhdatas}')
            for qhdata in qhdatas:
                qhs_list = qhdata.split('\n')
                # print(qhs_list)
                for qh in qhs_list:
                    qhChain = {}
                    regx = r'\S+'
                    qh_list = re.findall(regx, qh, re.MULTILINE)
                    # print(qh_list)
                    if len(qh_list) > 2:
                        for i_headOrTail in [0, 1]:
                            qhChain[i_headOrTail] = road.switchBreakChainageToNoBreak(qh_list[i_headOrTail], prjpath)
                            chainageA_nobreak = road.switchBreakChainageToNoBreak(chainageA, prjpath)
                            chainageB_nobreak = road.switchBreakChainageToNoBreak(chainageB, prjpath)
                            if min(chainageA_nobreak, chainageB_nobreak) <= qhChain[i_headOrTail] <= max(chainageA_nobreak, chainageB_nobreak):
                                if i == 3:  # 左右幅判断
                                    if float(qh_list[-1]) == 0:
                                        return qh_list[i_headOrTail]
                                    elif float(qh_list[-1]) == -1 and float(lOrRSideOfsubgrade) == 1:
                                        return qh_list[i_headOrTail]
                                    elif float(qh_list[-1]) == 1 and float(lOrRSideOfsubgrade) == 2:
                                        return qh_list[i_headOrTail]
                                else:
                                    return qh_list[i_headOrTail]
                    else:
                        continue
            i = i + 1
        chainageA_nobreak = road.switchBreakChainageToNoBreak(chainageA, prjpath)
        chainageB_nobreak = road.switchBreakChainageToNoBreak(chainageB, prjpath)
        try:
            (chainageA_nobreak + chainageB_nobreak) / 2
        except:
            print(chainageA_nobreak,chainageB_nobreak)
        return road.switchNoBreakToBreakChainage((chainageA_nobreak+chainageB_nobreak)/2, prjpath)
def findSlopeFromLine(linedata, i_slopeStart, i_slopeEnd, platformFilters='default', slopeFilters='default'):
    '''
    功能：得到给定边坡范围边坡信息（i_slopeStart和i_slopeEnd表示边坡在linedata中的开始和结束的位置）
    :param linedata:线段信息，格式要像3dr左侧或右侧横断面格式，组数、平距、高差.....
    :param i_slopeStart:边坡开始于第i_slopeStart组（平距+高差为一组）
    :param i_slopeEnd:边坡止于第i_slopeEnd组（平距+高差为一组）
    :param platformFilters:平台判定条件
    :param slopeFilters:边坡判定条件
    :return:[
             [坡高 第1级 S宽度 S高度 S坡度 P宽度 P高度 P边度],
             [坡高 第2级 S宽度 S高度 S坡度 P宽度 P高度 P边度],
             ...
             [坡高 第i级 S宽度 S高度 S坡度 P宽度 P高度 P边度],
             ]
             坡高指边坡总高，S指边歧，P指平台
             2、不符合条件时返回res=[]
     注：坡度为0时，判断为分离式路基；坡度为0段高度不计入坡高，级数
    '''

    if platformFilters == 'default':  # 平台判定条件
        drainageFilter1 = ['0<width', '10<abs(gradient)<=9999']  # 第1条边判定条件
        platformFilter_list = [drainageFilter1]
    if slopeFilters == 'default':  # 边坡判定条件
        drainageFilter1 = ['abs(height)>0', '0<=abs(gradient)<=10']  # 第1条边判定条件
        slopeFilter_list = [drainageFilter1]
    regx = r'-?\d+\.?\d*'
    pointsOfLinedata = re.findall(regx, linedata, re.MULTILINE)
    print(pointsOfLinedata)
    res = []
    wlist = {}
    hlist = {}
    glist = {}
    isSlope = {}
    isPlatform = {}
    slopeLevel = 1
    i_slopeLevel = 0
    i_slopeEnd = int(i_slopeEnd)
    i_slopeStart = int(i_slopeStart)
    heightSum=0
    if i_slopeEnd <= i_slopeStart:
        print('findSlopeFromLine 函数参数错误。', i_slopeStart, i_slopeEnd)
        return res
    for i in range(i_slopeStart, i_slopeEnd):
        if abs(float(pointsOfLinedata[(i + 2) * 2 - 1])) - abs(float(pointsOfLinedata[(i + 2 - 1) * 2 - 1])) < 0:
            print("挡墙")
            return res  # 大概率是挡墙
        # 一、计算宽度、高度、坡度
        widthOfPoint = float(pointsOfLinedata[(i + 2) * 2 - 1]) - float(pointsOfLinedata[(i + 2 - 1) * 2 - 1])
        widthOfPoint = abs(float('{:.3f}'.format(widthOfPoint)))
        heightOfPoint = float(pointsOfLinedata[(i + 2) * 2]) - float(pointsOfLinedata[(i + 2 - 1) * 2])
        heightOfPoint = float('{:.3f}'.format(heightOfPoint))
        heightSum = heightSum + heightOfPoint
        try:
            gradientOfPint = widthOfPoint / heightOfPoint
            gradientOfPint = float('{:.3f}'.format(gradientOfPint))
            if gradientOfPint == 0:  # 分离式路基边坡高度处理
                heightSum = heightSum - heightOfPoint
        except ZeroDivisionError:
            gradientOfPint = 9999
        # print(widthOfPoint,heightOfPoint,gradientOfPint)
        # 二、处理重合点；合并坡比相近线段
        if widthOfPoint == 0 and heightOfPoint == 0:
            continue
        try:
            temp = abs(glist[i_slopeLevel - 1] - gradientOfPint)
        except:
            wlist[i_slopeLevel] = widthOfPoint
            hlist[i_slopeLevel] = heightOfPoint
            glist[i_slopeLevel] = gradientOfPint
        else:
            if abs(glist[i_slopeLevel - 1] - gradientOfPint) <= 0.05:  # 合并坡比相近线段
                i_slopeLevel = i_slopeLevel - 1
                wlist[i_slopeLevel] = widthOfPoint + wlist[i_slopeLevel]
                hlist[i_slopeLevel] = heightOfPoint + hlist[i_slopeLevel]
            else:
                wlist[i_slopeLevel] = widthOfPoint
                hlist[i_slopeLevel] = heightOfPoint
                glist[i_slopeLevel] = gradientOfPint
        [width, height, gradient] = [widthOfPoint, heightOfPoint, gradientOfPint]
        # 三、根据给定条件判定平台、边坡
        for m in range(len(slopeFilter_list)):
            for n in range(len(slopeFilter_list[m])):
                if eval(slopeFilter_list[m][n]):
                    try:
                        isSlope[i_slopeLevel] = True and isSlope[i_slopeLevel]
                    except:
                        isSlope[i_slopeLevel] = True
                    # print('this is slope')
                else:
                    isSlope[i_slopeLevel] = False
        for m in range(len(platformFilter_list)):
            for n in range(len(platformFilter_list[m])):
                if eval(platformFilter_list[m][n]):
                    try:
                        isPlatform[i_slopeLevel] = True and isPlatform[i_slopeLevel]
                    except:
                        isPlatform[i_slopeLevel] = True
                    # print('this is platform')
                else:
                    isPlatform[i_slopeLevel] = False
        #四、输出res
        '''
            1先标记平台或者边坡，isSlope[i]
            2合并不同同一坡比边坡或平台
            3不同坡比边坡，边坡级数+1；不同坡比平台，级数不变
            4第一个pointdata存放一组边坡和平台数据（缺失部位用0补齐）
        '''
        if isSlope[i_slopeLevel] == isPlatform[i_slopeLevel]:
            print('边坡、平台规则有重叠')
        elif isSlope[i_slopeLevel] == True:
            res_slopei = [heightSum, slopeLevel, wlist[i_slopeLevel], hlist[i_slopeLevel], glist[i_slopeLevel], 0, 0, 0]
            res.append(res_slopei)
            slopeLevel = slopeLevel + 1
        elif isPlatform[i_slopeLevel] == True:
            try:
                res_slopei[-3] = wlist[i_slopeLevel]
                res_slopei[-2] = hlist[i_slopeLevel]
                res_slopei[-1] = glist[i_slopeLevel]
            except:
                res_slopei = [heightSum, slopeLevel - 1, 0, 0, 0, 0, 0, 0]
                res_slopei[-3] = wlist[i_slopeLevel]
                res_slopei[-2] = hlist[i_slopeLevel]
                res_slopei[-1] = glist[i_slopeLevel]
                res.append(res_slopei)
                res_slopei = []
        i_slopeLevel = i_slopeLevel + 1

    # 修改坡高
    for i, tempslope in enumerate(res):
        res[i][0] = heightSum
    return res
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
    wlist={}
    hlist={}
    glist={}
    try:
        while i <float(pointsOfLinedata[0])-1:
            if abs(float(pointsOfLinedata[(i+2)*2-1]))-abs(float(pointsOfLinedata[(i+2-1)*2-1]))<0:
                print("挡墙")
                return False    #大概率是挡墙
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
            wlist[i]=widthOfPoint
            hlist[i]=heightOfPoint
            glist[i]=gradientOfPint
            [width, height, gradient] = [widthOfPoint, heightOfPoint, gradientOfPint]
            if eval(Filter[m][0]):
                i_last=i
                if eval(Filter[m][1]):
                    if eval(Filter[m][2]):
                        m=m+1
                        if m == len(Filter):    #判定为边沟/排水沟条件
                            res.append(i-len(Filter)+1)
                            res.append(len(Filter))
                            j=res[0]
                            while j<=i:
                                res.append(wlist[j])
                                res.append(hlist[j])
                                res.append(glist[j])
                                # res.append(float(pointsOfLinedata[(j+2)*2-1]))
                                # res.append(float(pointsOfLinedata[(j + 2) * 2]))
                                j=j+1
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
                i = i - 1
            i=i+1
        if len(res)!=0:
            # print(f'边沟{res}')
            return res
        else:
            return False
    except:
        return False
def getDataFromTf(pathOfTF,chainage='all'):
    #功能从tfpath中查找桩号为chainage的数据，桩号缺省或桩号为all时查找全部桩号
    prjpath = pathOfTF
    chainage = chainage.strip()
    if os.path.exists(prjpath):
        if chainage.lower() == 'all':
            regx = r'^[\t\f ]*[a-zA-Z]?(?:\d+|\d+\.\d+).+[\n\r]'  # 将tf中所有桩号信息分组提取
        elif len(chainage) == 0:
            road.gui_filenotfine(f'函数getDataFromTf中桩号{chainage}为空')
            return ''
        else:
            temp = road.cutInvalidWords_chainage(chainage)
            try:
                chainage = temp[0] + temp[1]
            except:
                road.gui_filenotfine(f'函数getDataFromTf中桩号{chainage}错误')
            if chainage.find('.') == -1:    #判断是整桩号还是含小数桩号
                regx = f'^[\t\f ]*[a-zA-Z]?(?:{chainage}(?:\.0+)?)[\t\f ]+.+[\n\r]' # 将tf中桩号chainage信息提取
            else:
                regx = f'^[\t\f ]*[a-zA-Z]?(?:{chainage}0*)[\t\f ]+.+[\n\r]'   # 将tf中桩号chainage信息提取
        if len(chainage) == 0:
            return ''
        else:
            file = open(prjpath, 'r')
            data_file = file.read().upper()
            cross_sections = re.findall(regx, data_file, re.MULTILINE)
            file.close()
            return cross_sections
    else:
        temp = road.gui_filenotfine(f'函数getDataFromTf中路径{prjpath}不存在')
        return ''
def getCrossSectionOf3dr(pathof3dr,chainage='all'):
    #查找pathof3dr中给定桩号的横断面信息cross_section，桩号缺省或桩号为all时查找全部桩号
    prjpath=pathof3dr
    chainage=chainage.strip()
    if os.path.exists(prjpath):
        if chainage.lower()=='all':
            regx=r'^[\t\f ]*[a-zA-Z]?(?:\d+|\d+\.\d+)[\t\f ]*[\n](?:.+[\n\r])+'   #提取3dr中横断面信息
        elif len(chainage)==0:
            pass
        else:
            temp=road.cutInvalidWords_chainage(chainage)
            try:
                chainage=temp[0]+temp[1]
            except:
                pass
            if chainage.find('.')==-1:
                regx = f'^[\t\f ]*[a-zA-Z]?(?:{chainage}(?:\.0+)?)[\t\f ]*[\n](?:.+[\n\r])+'
            else:
                regx =f'^[\t\f ]*[a-zA-Z]?(?:{chainage}0*)[\t\f ]*[\n](?:.+[\n\r])+'
        if len(chainage)==0:
            return ''
        else:
            file=open(prjpath,'r')
            data_file=file.read().upper()
            cross_sections=re.findall(regx,data_file,re.MULTILINE)
            file.close()
            return cross_sections
    else:
        temp=road.gui_filenotfine(prjpath)
def getChainageFromChainagetable(db,chainage,breakchain=False):
    #功能:找出桩号chainage（变量）在数据库db数据表Chainage（常量）中对应的桩号，
    #breakchain=False,表示给定桩号不含断链，且返回字段chainage_naBreakChain中对应的桩号，否则返回字段chainage中桩号
    with mysql.UsingMysql(log_time=False, db=db) as um:
        if breakchain==True:
            sql = f"select chainage from chainage "
        else:
            sql = "select chainage_noBreakChain  from chainage"
        um.cursor.execute(sql)
        chainage_list =road.cutInvalidWords_chainage(chainage)
        # print(chainage_list)
        try:
            chainage = chainage_list[0] + chainage_list[1]
        except:
            return ''
        else:
            chainageValuesInTable_list_dic = um.cursor.fetchall()
            chainageValuesInTable_list = [item[key] for item in chainageValuesInTable_list_dic for key in item]
            chainageValuesInTable_list_join = '\t'.join(chainageValuesInTable_list).upper()
            # print(chainageValuesInTable_list_join)
            if chainage.find('.') == -1:  # 判断是整桩号还是含小数桩号
                regx = f'(?<!\w)({chainage}(?:\.0+))(?!\w)'  # 将tf中桩号chainage信息提取
            else:
                regx = f'(?<!\w)({chainage}0*)(?!\w)'
            res = re.findall(regx, chainageValuesInTable_list_join, re.MULTILINE)
            return res
def setupChainageTable(prjname,prjpath):
    #功能：建立chainage表
    #步骤：
        # 1 查找纬地项目文件prj中3dr文件路径
        # 2 提取3dr文件中桩号
        # 3 将3dr中的桩号，存入数据表chainage中
    path=prjpath
    prjname=prjname

    # 1 查找纬地项目文件prj中3dr文件路径
    path=road.findXPathFromPrj(path,'3dr')

    # 2 提取3dr文件中桩号
    try:
        file=open(path,'r')
    except:
        msgbox=road.gui_filenotfine(path)
    else:
        filedata = file.read()
        regx = r'^\s*(\w{0,1}\d+\.\d+|\w{0,1}\d+)\s*\n' #提取3dr中桩号的正则表达式
        keyslist = re.findall(regx, filedata, re.MULTILINE)
        file.close()
    # res=TransEiDatToHint3dr.whetherContainTheKeyInDmxfile(34676.4,path)
    # print(res)
        temp=road.creatMysqlChainageTable(prjname)
        conn = pymysql.connect(user = "root",passwd = "sunday")#,db = "mysql")
        cursor = conn.cursor()
        conn.select_db(prjname)
        sql='insert into chainage values(%s,%s,%s,%s)'
        i=1
        # 3 装3dr中的桩号，存入数据表key中
        for key in keyslist:
            insert = cursor.execute(sql,(i,i-1,key,0))
            i=i+1
        cursor.close()
        conn.commit()
        conn.close()
        print('chainage数据导入成功')
def creatMysqlSlopeProtecTypeTable(databaseName):
    '''
    功能：在databaseName数据库中新建边坡防护类型表settheprotectiongtypeofslope
    表中字段说明：
        chainagemin 最小桩号（含断链）
        最大级数min 为本断面的最大级数的最小值
        高度min   本级边坡高度的最小值
        坡高min   为本断面的边坡高度（每级边坡高度之和）的最小值
    :param databaseName:
    :return:
    '''
    tablename = 'settheprotectiongtypeofslope'
    prjname = databaseName
    with mysql.UsingMysql(log_time=False, db=prjname) as um:
        # conn = pymysql.connect(user="root", passwd="sunday")
        # cursor = conn.cursor()
        # conn.select_db(prjname)
        # cursor.execute(f'drop table if exists {tablename}')
        um.cursor.execute(f'drop table if exists {tablename}')
        sql = """CREATE TABLE IF NOT EXISTS `settheprotectiongtypeofslope` (
            `id` INT(2) NOT NULL AUTO_INCREMENT,
            `chainagemin` VARCHAR(50),
            `chainagemax` VARCHAR(50),
            `坡度min` Float(10),
            `坡度max` Float(10),
            `第i级min` INT(2),
            `第i级max` INT(2),
            `最大级数min` INT(2),
            `最大级数max` INT(2),
            `高度min` Float(10) ,
            `高度max` Float(10) ,
            `坡高min` Float(10),
            `坡高max` Float(10),
            `地质` VARCHAR(50),
            `防护类型` VARCHAR(50),
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
        um.cursor.execute(sql)
        slopedataForTable = ((1, 0, 100000, -5, -1, 1, 1, 1, 10, -3, 0, -3, 0, '', '填方喷播植草灌护坡'),
                             (2, 0, 100000, -5, -1, 1, 10, 1, 10, -8, -0, -8, -3, '', '填方方格网植草护坡'),
                             (3, 0, 100000, -5, -1, 1, 10, 1, 10, -60, -0, -60, -8, '', '填方拱形骨架衬砌护坡'),
                             (4, 0, 100000, 0.5, 1.5, 1, 10, 1, 10, 0, 4, 0, 4, '', '挖方喷播植草护坡'),
                             (5, 0, 100000, 0.5, 1.5, 1, 10, 1, 10, 0, 10, 4, 10, '', 'CF网植草防护'),
                             (6, 0, 100000, 0.5, 1.5, 1, 2, 2, 2, 0, 20, 10, 21, '', '挂双网喷射有机基材'),
                             (7, 0, 100000, 0.1, 1.5, 1, 3, 3, 3, 0, 30, 20, 31, '', '锚杆框架梁植草防护'),
                             (8, 0, 100000, 0.1, 1.5, 1, 10, 4, 10, 0, 100, 30, 100, '', '深挖路基'),
                             (9, 0, 100000, 1.5, 9999, 1, 10, 1, 10, 0, 100, 0, 100, '', '特殊挖方边坡'),
                             (10, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -15, -1, -15, -1, '', '路肩墙'),
                             (11, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -1, 0, -1, -0, '', '护肩'),
                             (12, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -14, -2, -34, 0, '', '路堤墙'),
                             (13, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -2, -1, -100, -0, '', '护脚'))
        sql = "insert into settheprotectiongtypeofslope values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        um.cursor.executemany(sql, slopedataForTable)
    print('settheprotectiongtypeofslope表创建成功V1.0')
def creatMysqlSlopeTable_v1(databaseName):
    #在databaseName数据库中新建边坡表Slope
    # 序号 chainage    左右侧(1/2) 位于边沟左右侧(0(无边沟)/1（边沟左侧）/2（边沟右内里）)	边坡类型（1填-1挖） 坡高 最大级数    【第i级平台	第i级平台坡度	第i级平台平距	第i级平台高度	第i级平台坐标x	第i级平台坐标y	第i级平台高程
                                                                                                               # 	第i级边坡	第i级边坡坡度	第i级边坡平距	第i级边坡高度	第i级边坡坐标x	第i级边坡坐标y	第i级边坡高程】
    tablename = 'slope'
    prjname=databaseName
    conn = pymysql.connect(user = "root",passwd = "sunday")#,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)
    cursor.execute(f'drop table if exists {tablename}')
    sql = """CREATE TABLE IF NOT EXISTS `slope` (
          `id` int(6) NOT NULL AUTO_INCREMENT,
          `chainage` varchar(50) NOT NULL ,
          `左右侧` int(1) NOT NULL ,
          `3dr中起始位置` int(3) ,
          `线段个数` int(3),
          `位于边沟左右侧` int(1) ,
          `边坡类型` int(1) ,
          `坡高` int(4) ,
          `最大级数` int(1) ,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
    cursor.execute(sql)
    for i in range(9):
        for name in ['S','P']:
            temp=str(i)+'级'+name
            sql=f'alter table {tablename} add {temp} float(10)'
            cursor.execute(sql)
            temp=name+'宽度'+str(i)
            sql=f'alter table {tablename} add {temp} float(10)'
            cursor.execute(sql)
            temp=name+'高度'+str(i)
            sql=f'alter table {tablename} add {temp} float(10)'
            cursor.execute(sql)
            temp=name+'坡度'+str(i)
            sql=f'alter table {tablename} add {temp} float(10)'
            cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    print('slope表创建成功1.0')
def creatMysqlSlopeTable(databaseName):
    #在databaseName数据库中新建边坡表Slope
    # 序号 chainage    左右侧(1/2) 位于边沟左右侧(0(无边沟)/1（边沟左侧）/2（边沟右内里）)	边坡类型（1填-1挖） 坡高 最大级数    【第i级平台	第i级平台坡度	第i级平台平距	第i级平台高度	第i级平台坐标x	第i级平台坐标y	第i级平台高程
                                                                                                               # 	第i级边坡	第i级边坡坡度	第i级边坡平距	第i级边坡高度	第i级边坡坐标x	第i级边坡坐标y	第i级边坡高程】
    tablename = 'slope'
    prjname=databaseName
    conn = pymysql.connect(user = "root",passwd = "sunday")#,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)
    cursor.execute(f'drop table if exists {tablename}')
    sql = """CREATE TABLE IF NOT EXISTS `slope` (
          `id` int(6) NOT NULL AUTO_INCREMENT,
          `chainage` varchar(50) NOT NULL ,
          `左右侧` int(1) NOT NULL ,
          `3dr中起始位置` int(3) ,
          `线段个数` int(3),
          `位于边沟左右侧` int(1) ,
          `边坡类型` int(1) ,
          `坡高` float(10) ,
          `最大级数` int(2) ,
          `第i级` int(2) ,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
    cursor.execute(sql)
    for i in range(1):
        for name in ['S','P']:
            temp=name+'宽度'
            sql=f'alter table {tablename} add {temp} float(10)'
            cursor.execute(sql)
            temp=name+'高度'
            sql=f'alter table {tablename} add {temp} float(10)'
            cursor.execute(sql)
            temp=name+'坡度'
            sql=f'alter table {tablename} add {temp} float(10)'
            cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    print('slope表创建成功V2.0')
def creatMysqlChainageTable(databaseName):
    #在databaseName数据库中新建chainage表、typeofslopeprot表
    prjname=databaseName
    conn = pymysql.connect(user="root", passwd="sunday")
    cursor = conn.cursor()
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {prjname} DEFAULT CHARSET utf8 COLLATE utf8_general_ci;')
    conn.select_db(prjname)
    cursor.execute('drop table if exists chainage')
    sql = """CREATE TABLE IF NOT EXISTS `chainage` (
          `id` int(6) NOT NULL AUTO_INCREMENT,
          `id_last` int(6) ,
          `chainage` varchar(50) NOT NULL,
          `chainage_noBreakChain` int(50) NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
    cursor.execute(sql)
    cursor.execute('DROP TABLE IF EXISTS typeofslopeprot')
    sql = '''CREATE TABLE IF NOT EXISTS typeofslopeprot(
        `id` INT(2) NOT NULL AUTO_INCREMENT,
        `坡度min` FLOAT(10),
        `坡度max` FLOAT(10), 
        `坡高min` FLOAT(10),
        `坡高max` FLOAT(10), 
        `防护类型` VARCHAR(50),
        PRIMARY KEY (`id`)
        )ENGINE=INNODB DEFAULT CHARSET=utf8;'''
    cursor.execute(sql)
    insertdatalist = [[1,-10,-1,-4,0,'绿化'],
                      [2,-10,-1,-20,-4,'拱形骨架护坡']]
    sql = "INSERT INTO typeofslopeprot VALUES(%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql, insertdatalist)
    cursor.close()
    conn.commit()
    conn.close()
def creatMysqlDrainageDitchTable(databaseName):
    #在databaseName数据库中新建drainageDitch表
    # chainage    左右侧 3dr中起始位置     线段个数   宽度1    高度1  坡度1  宽度2    高度2  坡度2...
    prjname=databaseName
    conn = pymysql.connect(user = "root",passwd = "sunday")#,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)
    cursor.execute('drop table if exists drainageDitch')
    sql = """CREATE TABLE IF NOT EXISTS `drainageDitch` (
          `id` int(6) NOT NULL AUTO_INCREMENT,
          `chainage` varchar(50),
          `左右侧` int(1) NOT NULL ,
          `3dr中起始位置` int(3) ,
          `线段个数` int(3),
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
    cursor.execute(sql)
    for i in range(9):
        temp='宽度'+str(i)
        sql=f'alter table drainageDitch add {temp} float(10)'
        cursor.execute(sql)
        temp='高度'+str(i)
        sql=f'alter table drainageDitch add {temp} float(10)'
        cursor.execute(sql)
        temp='坡度'+str(i)
        sql=f'alter table drainageDitch add {temp} float(10)'
        cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
def findXPathFromPrj(prjpath,typeOfFindX):
    #查找纬地项目文件prjpath中X文件路径，例FindXPathFromPrj(prjpath,3dr)
    path_Dmxfile=prjpath
    typeOfFindX=typeOfFindX.lower()
    try:
        prjfile=open(path_Dmxfile,'r')
    except:#except FileNotFoundError:
        msgbox = gui_filenotfine(path_Dmxfile)
        sys.exit()
    else:
        data_prj=prjfile.read()
        prjfile.close()
        data_prj=data_prj.lower()
        # regx = f'\*\.{typeOfFindX}\).*=\s*(.*)\s*(?=\n)'
        regx = roadglobal.regx_FindXPathFromPrj(typeOfFindX)
        res = re.findall(regx, data_prj, re.MULTILINE)
        # print(f'res:{res}')
        try:
            res[0]=res[0].strip()
        except:
            msgbox = gui_filenotfine(f'findXPathFromPrj {typeOfFindX} path不存在')
            return ""
        if len(res[0])>0:
            if os.path.exists(res[0]):
                return res[0]
            else:
                # regx=r'[\u4e00-\u9fa5_a-zA-Z0-9]+.\w+'
                # temp=re.findall(regx,res[0],re.MULTILINE)
                res[0]=res[0].replace('/','\\')
                res[0]=res[0].split('\\')
                res[0]=res[0][len(res[0])-1].strip()
                if res[0].find('.') == -1:
                    msgbox = gui_filenotfine(f'findXPathFromPrj {typeOfFindX} path:{res[0]}')
                    return ""
                else:
                    path_Dmxfile=path_Dmxfile.replace('/','\\')
                    path_dmxfilelist=path_Dmxfile.split('\\')
                    path_dmxfilelist[len(path_dmxfilelist)-1]=res[0]
                    xpath='\\'.join(path_dmxfilelist)
                # print('res',res)
                # print('temp',temp)
                # print('temppath',temppath)

                if os.path.exists(xpath):
                    # print(f'findXPathFromPrj {typeOfFindX} path:', xpath)
                    return xpath
                else:
                    msgbox=gui_filenotfine(f'findXPathFromPrj {typeOfFindX} path:{xpath}')
                    return ""
        else:
            return res[0]
def cutInvalidWords_chainage(chainage):
    #去除桩中无效数字或者字母，如输入A20.010 ，输出res  (res[0]=A,res[1]=20.01);20.010 ，输出res  (res[0]='',res[1]=20.01)
    res=[]
    chainage=chainage.strip()
    regx=r'(?<!\S)[a-zA-Z]?(\d+(?:\.\d*)?)(?!\S)'
    temp1=re.findall(regx,chainage,re.MULTILINE)
    # print('ctu', temp1)
    # print(f'temp1:{temp1}')
    try:
        temp = str(temp1[0])
    except:
        return res
    else:
        newtemp = temp
        i = 0
        try:
            while float(temp) == float(newtemp):
                newtemp = temp[0:len(temp) - i]
                i = i + 1
        except:
            pass
        temp1[0]= temp[0:len(temp) - i + 2]
        # temp1[0]='{:g}'.format(float(temp1[0]))
        # print(f'temp1[0]:{temp1[0]}')
        regx = r'(?<!\S)([a-zA-Z]?)\d+(?:\.\d*)?(?!\S)'
        temp2 = re.findall(regx, chainage, re.MULTILINE)
        res.append(temp2[0].upper())
        res.append(temp1[0])
        return res
def gui_filenotfine(path):
    # 功能：path文件不存在提示框
    rootb = tk.Tk()
    # 创建一个文本Label对象
    textLabel = Label(rootb,  # 将内容绑定在  root 初始框上面
                      text=f"{path}文件不存在",
                      justify=LEFT,  # 用于 指明文本的 位置
                      padx=10)  # 限制 文本的 位置 , padx 是 x轴的意思 .
    textLabel.pack(side=LEFT)  # 致命 textlabel 在初识框 中的位置
    mainloop()
