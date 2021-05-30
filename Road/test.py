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
from operator import itemgetter
import json
import gui_confirm
from tkinter import simpledialog

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
            i = 2
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
            print(getattr(obj, 'lineEdit_prjpath_1'))

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
            name, salary, age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(self.ui,
                          '统计结果',
                          f'''薪资20000 以上的有：\n{salary_above_20k}
                    \n薪资20000 以下的有：\n{salary_below_20k}'''
                          )






if __name__ == "__main__":
    mylist = [1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    # myset = set(mylist)
    # for item in myset:
    #     print("the %d has found %d" % (item, mylist.count(item)))

    from collections import Counter
    # a=Counter([1,2,2,2,2,3,3,3,4,4,4,4])
    # print(a)
    # print(type(a))

    # xya_list = [[1,2],[1,2],[1,3],[1,2],[1,5]]
    # a = Counter(xya_list)
    # #
    # # a = xya_list.count([1,2])
    # print(a)

    # set_list = set(xya_list)
    # print(set_list)
    # print(type(set_list))

    # xya_list = [[1, 2], [1, 2], [1, 3], [1, 2], [1, 5]]
    # set_list = set(xya_list)
    # print(set_list)

    line_new = []
    xya_list = [[1, 2], [1, 2], [1, 3], [1, 2], [1, 5]]
    # [line_new.append(i) for i in xya_list if not i in line_new]
    # print(line_new)

    # line_new = xya_list[0:2]
    # print(line_new)

    xya_list = xya_list[1:3]
    print(xya_list)