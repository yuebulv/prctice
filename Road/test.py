import TransEiDatToHint3dr
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import os
import road
import pymysql
import math
import mysql
import copy
import glob
import roadglobal
import gui_confirm
from tkinter import filedialog
# import filedialog
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

'''
下一步改进方向
1、断链处理存在问题
    处理方法1）改进现在代码
            2）重新写函数，将原路线桩号全部转为不含断链桩号，在成果中将所有桩号转为含断链桩号
2、增加统计路面数量功能
            

'''

if __name__ == "__main__":
    a = eval(1/2)
    print(a)