from tkinter import *
import tkinter as tk
import os
import road
import pymysql
import math
import mysql
import copy
import glob
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qfile

class Stats:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        qfile_stats = Qfile("ui/main.ui")
        qfile_stats.open(Qfile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)
        self.ui.actionOpenFile.triggered.connect(self.openPrjFile)



        # self.ui.button.clicked.connect(self.handleCalc)
    def openPrjFile(self):
        root = tk.Tk()
        root.withdraw()
        folderpath = filedialog.askdirectory(title='请选择prj文件所在文件夹')
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

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()


# if __name__ == "__main__":
#     root = Tk()
#     root.geometry('400x100+200+300')
#     root.title("gui")
#     app = Appliction(root)
#     root.mainloop()
