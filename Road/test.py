from tkinter import *
import tkinter.filedialog
import tkinter as tk
import os
import road
import pymysql
import math
import mysql
import copy
import roadglobal
import glob
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
import tkinter.messagebox

class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        qfile_stats = QFile("../ui/main.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)
        self.ui.action_openprj.triggered.connect(self.openPrjFile)
        self.ui.pushButton_quit.clicked.connect(self.quitSoftware)
        # self.ui.button.clicked.connect(self.handleCalc)
    def openPrjFile(self):
        root = tk.Tk()
        root.withdraw()
        folderpath = tkinter.filedialog.askdirectory(title='请选择prj文件所在文件夹')
        os.chdir(folderpath)
        for prjfile in glob.glob('*.prj'):
            prjpath = folderpath + '\\' + prjfile
            if os.path.exists(prjpath) == False:
                msgbox = road.gui_filenotfine(f'{prjpath} path:不在存在')
                continue
            prjpath = prjpath.replace('/', '\\')
            slopefilepath_list = prjpath.split('\\')
            regx = r'(.+)(?=\.\w+)'
            prjname = re.findall(regx, slopefilepath_list[-1])[0]
            prjname = prjname.replace('+', '')

            self.ui.lineEdit_prjname_1.setText(prjname)
            self.ui.lineEdit_prjpath_1.setText(prjpath)
            i=2
            uiWidget = f"lineEdit_prjname_{i}"
            # self.ui.uiWidget.setText(prjname)
            # self.ui.setAttribute(uiWidget, prjname)
            # setattr(self.ui, uiWidget, prjname)
            # print(self.ui.lineEdit_prjname_2.text)

            obj = self.ui
            print(self.ui.__getattribute__('lineEdit_prjpath_1'))
            print(dir(obj))
            # obj.lineEdit_prjname_3.setText(prjname)
            setattr(obj, 'lineEdit_prjname_2', prjname)
            print(obj)
            print(getattr(obj,'lineEdit_prjpath_1'))
    def quitSoftware(self):
        sys.exit()
    def handleCalc(self):
        info = self.ui.textEdit.toPlainText()

        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')

            parts = [p for p in parts if p]
            name,salary,age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(self.ui,
                    '统计结果',
                    f'''薪资20000 以上的有：\n{salary_above_20k}
                    \n薪资20000 以下的有：\n{salary_below_20k}'''
                    )

# app = QApplication([])
# stats = Stats()
# stats.ui.show()
# app.exec_()


def insert_dic_data_to_table(prjname, tableName, pama_dic):
    '''

    :param prjname: 数据库名称
    :param pama_dic: 需要插入的数据，需要是字典类型
    :param tableName:
    :return:
    '''
    # 5.3.3 C型急流槽(挖方平台截水沟到边沟）
    # 根据挖方平台截水沟段落、截水沟间距、纵坡方向判断
    # 方法：1）得到挖方段落；2）以挖方段落最高一级中间为准，按给定间距向两端设置急流槽；3）判断急流槽坡度，高度；4）输出急流槽桩号，第i级，高度，坡度，长度，C型急流槽
    # 不需考虑平台截水沟纵坡，两端截水沟通过调整沟底纵坡汇入急流槽
    # 此方案对于纵坡较大，同一段有多处山峰时不适用，后续需要改进。


def set_slope_rapid_gutter(database_name, prjpath):
    slopefilepath = r'D:\新建文件夹\E\rapidgutters.txt'
    outputslopefile = open(slopefilepath, 'w')
    SlopeLevel_setInterceptingDitch = [roadglobal.embankmentSlopeLevel_setInterceptingDitch,
                                       roadglobal.cuttingSlopeLevel_setInterceptingDitch]
    rapidGutter_spacing = [roadglobal.embankment_rapidGutter_spacing, roadglobal.cutting_rapidGutter_spacing]
    with mysql.UsingMysql(log_time=True, db=database_name) as um:
        for lorR_drain in [1]:
            for lorR_slope_drainage in [1]:
                # 5.3.3.1 得到挖方最高一级段落；
                rapidGutterChainages_list = []
                sql = f'''
                    SELECT 
                        *
                    FROM 
                        platformdrainingroup
                    WHERE platformdrainingroup.`左右侧`={lorR_drain}
                    AND 
                        platformdrainingroup.`位于边沟左右侧`={lorR_slope_drainage}
                    AND 
                        platformdrainingroup.第i级=1
                    AND 
                        platformdrainingroup.最大级数max>1
                    ORDER BY 
                       id ASC;'''
                um.cursor.execute(sql)
                data_slopeLevel1_dic_list = um.cursor.fetchall()  # 第1级段落
                print(f'data_slopeLevel1_dic_list:{data_slopeLevel1_dic_list}')
                sql = f'''
                    SELECT 
                        *
                    FROM 
                        platformdrainingroup
                    WHERE platformdrainingroup.`左右侧`={lorR_drain}
                    AND 
                        platformdrainingroup.`位于边沟左右侧`={lorR_slope_drainage}
                    AND 
                        platformdrainingroup.第i级=最大级数max-1 
                    ORDER BY 
                       id ASC;'''
                um.cursor.execute(sql)
                data_dic_list = um.cursor.fetchall()  # 最大级段落
                print(data_dic_list)
                for i in range(0, len(data_dic_list)):
                    startChainage = data_dic_list[i]['起点']
                    endChainage = data_dic_list[i]['止点']
                    startChainage_noBreak = road.switchBreakChainageToNoBreak(startChainage, prjpath)
                    endChainage_noBreak = road.switchBreakChainageToNoBreak(endChainage, prjpath)
                    slopeLevel = int(data_dic_list[i]['第i级'])
                    rapidGutterChainage = int((startChainage_noBreak + endChainage_noBreak)/2)
                    print(f'基准rapidGutterChainage:{rapidGutterChainage}')
                    # 5.3.3.2）以挖方段落最高一级中间为准，按给定间距向两端设置急流槽；
                    for j in range(0, len(data_slopeLevel1_dic_list)):
                        startChainage_slopeLevel1 = data_slopeLevel1_dic_list[j]['起点']
                        endChainage_slopeLevel1 = data_slopeLevel1_dic_list[j]['止点']
                        startChainage_noBreak_slopeLevel1 = road.switchBreakChainageToNoBreak(startChainage_slopeLevel1, prjpath)
                        startChainage_noBreak_slopeLevel1 = int(startChainage_noBreak_slopeLevel1)
                        endChainage_noBreak_slopeLevel1 = road.switchBreakChainageToNoBreak(endChainage_slopeLevel1, prjpath)
                        endChainage_noBreak_slopeLevel1 = int(endChainage_noBreak_slopeLevel1)
                        if startChainage_noBreak_slopeLevel1 <= startChainage_noBreak <= endChainage_noBreak_slopeLevel1:
                            print(f'startChainage_noBreak_slopeLevel1:{startChainage_noBreak_slopeLevel1}')
                            print(f'endChainage_noBreak_slopeLevel1:{endChainage_noBreak_slopeLevel1}')
                            rapidGutterChainage_list = sorted(list(range(rapidGutterChainage, startChainage_noBreak_slopeLevel1,
                                                                         -rapidGutter_spacing[lorR_slope_drainage-1])))
                            temptList = list(range(rapidGutterChainage, endChainage_noBreak_slopeLevel1, rapidGutter_spacing[lorR_slope_drainage-1]))
                            # 得到了急流槽桩号
                            rapidGutterChainage_list.extend(temptList[1:])
                            rapidGutterChainages_list.extend(rapidGutterChainage_list)
                            print(f'rapidGutterChainages_list:{rapidGutterChainages_list}')
                            break

                # 5.3.3.3）判断急流槽坡度，高度；
                rapidGutters_dic_list = []
                for rapidGutterChainage_noBreak in rapidGutterChainages_list:
                    nearbyChainageData = road.get_rapid_gutter_parameter(rapidGutterChainage_noBreak, 'slope',
                                                                         database_name, prjpath, lorR_drain,
                                                                         lorR_slope_drainage, isBreakchainage=False)
                    print(f'nearbyChainageData:{nearbyChainageData}')
                    if nearbyChainageData[0] is None and nearbyChainageData[1] is None:
                        continue
                    elif nearbyChainageData[0] is None:
                        rapidGutter_dic_list = nearbyChainageData[1]
                    elif nearbyChainageData[1] is None:
                        rapidGutter_dic_list = nearbyChainageData[0]
                    else:
                        rapidGutter_dic_list = insert_slope_value_betweent_chainageAB(rapidGutterChainage_noBreak, nearbyChainageData, prjpath)
                    rapidGutters_dic_list.append(rapidGutter_dic_list)
                # 5.3.3.4）输出急流槽桩号，第i级，高度，坡度，长度，C型急流槽
                print('rapidGutters_dic_list:')
                for temp in rapidGutters_dic_list:
                    print(temp)
                try:
                    outputslopefile.write(str(list(rapidGutters_dic_list[0][0].keys())))
                    outputslopefile.write('\n')
                except:
                    pass
                for temp1 in rapidGutters_dic_list:
                    for temp in temp1:
                        outputslopefile.write(str(list(temp.values())))
                        outputslopefile.write('\n')
    outputslopefile.close()


def insert_slope_value_betweent_chainageAB(rapidGutterChainage_noBreak, nearbyChainageData, prjpath):
    # 默认相邻断面中坡高较高断面，最大级数较大；默认S坡度、P坡度相信断面一致且以较高断面对应坡度一致；所求断面边坡分级高度与较高断面一致。
    # 默认nearbyChainageData有两组边坡，每组边坡最小边坡级数为1级；
    # 例：断面A边坡有[1,2]级，断面C[1,2,3,4]；
    # 那中间所求断面B，第1级为AB共有级：平均值法；
    # 第[3,4]级为断面C独有：分级高度，坡度，平台宽度、坡度与C断面一致，
    # 第[2]级为过渡级，边坡高度=总高度-第[1,3,4]级，边坡坡度采用平均值法
    # [[第1级dic]...[第i级dic]]

    if nearbyChainageData == '':
        return ''
    # 给nearbyChainageData排序
    nearbyChainageData_copy =copy.deepcopy(nearbyChainageData)
    for i in range(0, len(nearbyChainageData_copy)):
        for j in range(0, len(nearbyChainageData_copy[i])):
            temp = nearbyChainageData_copy[i][j]['第i级']
            try:
                nearbyChainageData[i][temp] = copy.deepcopy(nearbyChainageData_copy[i][j])
            except IndexError:
                nearbyChainageData[i].append(nearbyChainageData_copy[i][j])
        nearbyChainageData[i] = nearbyChainageData[i][1:]
    # for i in range(0, len(nearbyChainageData)):
    #     for j in range(0, len(nearbyChainageData[i])):
    #         print(f'nearbyChainageData[i][j]:{nearbyChainageData[i][j]}')

    res = []
    data_dic = []
    height_B_sum = 0
    # maxLevel_1 = nearbyChainageData[0][0]['最大级数']
    # maxLevel_2 = nearbyChainageData[1][0]['最大级数']
    # if maxLevel_1 <= maxLevel_2:
    #     index_list = [0, 1]
    # else:
    #     index_list = [1, 0]
    maxLevel_1 = nearbyChainageData[0][0]['坡高']
    maxLevel_2 = nearbyChainageData[1][0]['坡高']
    if abs(maxLevel_1) <= abs(maxLevel_2):
        index_list = [0, 1]
    else:
        index_list = [1, 0]

    rapidGutter_dic = copy.deepcopy(nearbyChainageData[0][0])
    rapidGutterChainage_Break = road.switchNoBreakToBreakChainage(rapidGutterChainage_noBreak, prjpath)
    rapidGutter_dic['chainage'] = rapidGutterChainage_Break
    # 更新rapidGutter_dic值

    temp1 = nearbyChainageData[index_list[0]][0]['坡高']
    temp1_chainage = nearbyChainageData[index_list[0]][0]['chainage']
    temp1_chainage = road.switchBreakChainageToNoBreak(temp1_chainage, prjpath)
    temp2 = nearbyChainageData[index_list[1]][0]['坡高']
    temp2_chainage = nearbyChainageData[index_list[1]][0]['chainage']
    temp2_chainage = road.switchBreakChainageToNoBreak(temp2_chainage, prjpath)

    rapidGutter_dic['坡高'] = round(abs((temp1 - temp2) / (temp2_chainage - temp1_chainage) *
                                      (rapidGutterChainage_noBreak - temp1_chainage)) * temp1 / temp1 + temp1, 3)
    # 那中间所求断面B，第1级为AB共有级：平均值法；
    coefficient_1 = abs((rapidGutterChainage_noBreak-temp1_chainage)/(temp2_chainage - temp1_chainage))
    coefficient_2 = abs((rapidGutterChainage_noBreak - temp2_chainage) / (temp2_chainage - temp1_chainage))
    for i in range(1, nearbyChainageData[index_list[0]][0]['最大级数']):
        rapidGutter_dic = copy.deepcopy(rapidGutter_dic)  # 如无此句，后修改rapidGutter_dic值会影响res中rapidGutter_dic结果
        rapidGutter_dic['第i级'] = i
        rapidGutter_dic['S高度'] = round(nearbyChainageData[index_list[0]][i]['S高度']*coefficient_1 + nearbyChainageData[index_list[1]][i]['S高度']*coefficient_2, 3)
        rapidGutter_dic['S坡度'] = round(nearbyChainageData[index_list[0]][i]['S坡度']*coefficient_1 + nearbyChainageData[index_list[1]][i]['S坡度']*coefficient_2, 3)
        rapidGutter_dic['S宽度'] = round(rapidGutter_dic['S高度']*rapidGutter_dic['S坡度'], 3)
        rapidGutter_dic['P高度'] = round(nearbyChainageData[index_list[0]][i]['P高度']*coefficient_1 + nearbyChainageData[index_list[1]][i]['P高度']*coefficient_2, 3)
        rapidGutter_dic['P坡度'] = round(nearbyChainageData[index_list[0]][i]['P坡度']*coefficient_1 + nearbyChainageData[index_list[1]][i]['P坡度']*coefficient_2, 3)
        rapidGutter_dic['P宽度'] = round(nearbyChainageData[index_list[0]][i]['P宽度']*coefficient_1 + nearbyChainageData[index_list[1]][i]['P宽度']*coefficient_2, 3)
        res.append(rapidGutter_dic)
        print(f'rapidGutter_dic1:{rapidGutter_dic}')
        # print(f'res1:{res}')
        height_B_sum += rapidGutter_dic['S高度']
    # 第[3,4]级为断面C独有：分级高度，坡度，平台宽度、坡度与C断面一致，
    cot_a = (nearbyChainageData[index_list[1]][0]['坡高']-nearbyChainageData[index_list[0]][0]['坡高'])/(temp2_chainage - temp1_chainage)
    l_BC = temp2_chainage-rapidGutterChainage_noBreak
    height_remain = cot_a*l_BC
    for i in range(nearbyChainageData[index_list[0]][0]['最大级数']+1, nearbyChainageData[index_list[1]][0]['最大级数']+1):
        height_sum = 0
        for j in range(i, nearbyChainageData[index_list[1]][0]['最大级数'] + 1):
            height_sum += nearbyChainageData[index_list[1]][j-1]['S高度']
        if abs(height_sum)-abs(height_remain) <= 0:  # B断面止点在过段级
            break
        else:
            rapidGutter_dic = copy.deepcopy(rapidGutter_dic)
            rapidGutter_dic['第i级'] = i
            rapidGutter_dic['S坡度'] = round(nearbyChainageData[index_list[1]][i-1]['S坡度'], 3)
            rapidGutter_dic['P高度'] = round(nearbyChainageData[index_list[1]][i-1]['P高度'], 3)
            rapidGutter_dic['P坡度'] = round(nearbyChainageData[index_list[1]][i-1]['P坡度'], 3)
            rapidGutter_dic['P宽度'] = round(nearbyChainageData[index_list[1]][i-1]['P宽度'], 3)
            if abs(height_sum-height_remain) <= abs(nearbyChainageData[index_list[1]][i-1]['S高度']):  # 最后一级
                rapidGutter_dic['S高度'] = round(height_sum-height_remain, 3)
                rapidGutter_dic['S宽度'] = round(rapidGutter_dic['S高度'] * rapidGutter_dic['S坡度'], 3)
                res.append(rapidGutter_dic)
                print(f'rapidGutter_dic2:{rapidGutter_dic}')
                height_B_sum += rapidGutter_dic['S高度']
                break
            else:
                rapidGutter_dic['S高度'] = round(nearbyChainageData[index_list[1]][i-1]['S高度'], 3)
                res.append(rapidGutter_dic)
                print(f'rapidGutter_dic3:{rapidGutter_dic}')
                height_B_sum += rapidGutter_dic['S高度']

    # 第[2]级为过渡级，边坡高度=总高度-第[1,3,4]级，边坡坡度采用平均值法
    rapidGutter_dic = copy.deepcopy(rapidGutter_dic)
    i = nearbyChainageData[index_list[0]][0]['最大级数']
    rapidGutter_dic['第i级'] = i
    i = i-1
    rapidGutter_dic['S高度'] = round(rapidGutter_dic['坡高']-height_B_sum, 3)
    rapidGutter_dic['S坡度'] = round((nearbyChainageData[0][i]['S坡度'] + nearbyChainageData[1][i]['S坡度']) / 2, 3)
    rapidGutter_dic['S宽度'] = round(rapidGutter_dic['S高度'] * rapidGutter_dic['S坡度'], 3)
    if abs(rapidGutter_dic['S高度'])+0.05 < abs(nearbyChainageData[index_list[1]][i]['S高度']):
        rapidGutter_dic['P高度'] = round(nearbyChainageData[index_list[0]][i]['P高度'], 3)
        rapidGutter_dic['P坡度'] = round(nearbyChainageData[index_list[0]][i]['P坡度'], 3)
        rapidGutter_dic['P宽度'] = round(nearbyChainageData[index_list[0]][i]['P宽度'], 3)
    else:
        rapidGutter_dic['P高度'] = round(nearbyChainageData[index_list[1]][i]['P高度'], 3)
        rapidGutter_dic['P坡度'] = round(nearbyChainageData[index_list[1]][i]['P坡度'], 3)
        rapidGutter_dic['P宽度'] = round(nearbyChainageData[index_list[1]][i]['P宽度'], 3)
    res.insert(i, rapidGutter_dic)
    print(f'rapidGutter_dic4:{rapidGutter_dic}')
    # 修改最大级数
    maxSlopeLevel = len(res)
    for i in range(0, maxSlopeLevel):
        res[i]['最大级数'] = maxSlopeLevel
    return res
    # print(f'res4:{res}')

if __name__ == "__main__":
    database_name = 'e'
    prjpath = r'D:\新建文件夹\E\e.prj'
    set_slope_rapid_gutter(database_name, prjpath)
