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


def tem():
    database_name = 'e'
    # table_name = 'slopeInGroup'
    # res = road.whether_table_in_database(database_name, table_name)
    # print(res)
    prjpath = r'D:\新建文件夹\E\e.prj'

    rapidGutterChainage_list = []
    with mysql.UsingMysql(log_time=True, db=database_name) as um:
        # 5.3.3.1 得到挖方最高一级段落；
        SlopeLevel_setInterceptingDitch=[roadglobal.embankmentSlopeLevel_setInterceptingDitch, roadglobal.cuttingSlopeLevel_setInterceptingDitch]
        rapidGutter_spacing = [roadglobal.embankment_rapidGutter_spacing, roadglobal.cutting_rapidGutter_spacing]
        for lorR_drain in [1, 1]:
            for lorR_slope_drainage in [2, 2]:
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
                            rapidGutterChainage_list.extend(temptList[1:])

                            print(f'rapidGutterChainage_list:{rapidGutterChainage_list}')
                            break
                # 5.3.3.3）判断急流槽坡度，高度；
                # 5.3.3.4）输出急流槽桩号，第i级，高度，坡度，长度，C型急流槽


        # print("-- 当前数量: %d " % data['total'])


if __name__ == "__main__":
    # for i in [1, 1]:
    #     for j in [1, 1]:
    #         print(i,j)
    tem()


