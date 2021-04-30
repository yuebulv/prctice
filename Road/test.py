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
import tkinter
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

def set_rapid_gutter_b():
    # 5.3.2 B型急流槽(填挖交界截水沟）
    # 1）填方排水沟段落；2）相邻断面CA/CB，沟心距GLA/GLB，沟底高HA/HB，坡度公式：((CB-CA)^2+(GLA+GLB)^2+(HA-HB)^2)^0.5/(HB-HA)；3）根据坡度判断是否设置急流槽。
    database_name = 'e'
    prjpath = r'D:\新建文件夹\E\e.prj'
    rapid_gutter_saved_path = r'D:\新建文件夹\E\rapidgutters_b.txt'
    lorR_slope_drainage = 1
    with mysql.UsingMysql(log_time=False, db=database_name) as um:
        for lorR_drain in [1, 2]:
            # 1）填方排水沟段落
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


if __name__ == "__main__":
    database_name = 'e'
    prjpath = r'D:\新建文件夹\E\e.prj'
    rapid_gutter_saved_path = r'D:\新建文件夹\E\rapidgutters.txt'
    road.set_slope_rapid_gutter(database_name, prjpath, rapid_gutter_saved_path)

    # temp = {'a':1,'b':2,'c':3}
    # del temp['A']
    # print(temp)

    # sql = f'''
    #       SELECT
    #           *
    #       FROM
    #           platformdrainingroup
    #       WHERE platformdrainingroup.`左右侧`={lorR_drain}
    #       AND
    #           platformdrainingroup.`位于边沟左右侧`={lorR_slope_drainage}
    #       AND
    #           platformdrainingroup.第i级=1
    #       AND
    #           platformdrainingroup.最大级数max>1
    #       ORDER BY
    #          id ASC;'''
    #
    # sql = f'''
    #       SELECT
    #           *
    #       FROM
    #           platformdrainingroup
    #       WHERE platformdrainingroup.`左右侧`={lorR_drain}
    #       AND
    #           platformdrainingroup.`位于边沟左右侧`={lorR_slope_drainage}
    #       AND
    #           platformdrainingroup.第i级=最大级数max-1
    #       ORDER BY
    #          id ASC;'''


